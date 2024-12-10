from dataclasses import dataclass

import traceback
import logging
import random
import time
import os
import sys
import importlib
import inspect

from typing import Dict, List, TYPE_CHECKING, Optional, Union
from .kea_pbtest import KeaPBTest
from kea.Bundle import Bundle
from uiautomator2.exceptions import UiObjectNotFoundError

from .utils import DEFAULT_POLICY, DEFAULT_EVENT_INTERVAL, DEFAULT_TIMEOUT, DEFAULT_EVENT_COUNT 

if TYPE_CHECKING:
    from .kea_pbtest import Rule, MainPath
    from .pdl_hm import PDL as HarmonyOS_PDL
from .pdl import PDL as Android_PDL

from .utils import INITIALIZER_MARKER, RULE_MARKER, MAINPATH_MARKER

from .property_decorator import rule, precondition, initializer, mainPath

@dataclass
class CHECK_RESULT:
    ASSERTION_ERROR = 0
    PASS = 1
    UI_NOT_FOUND = 2
    PRECON_INVALID = 3

@dataclass
class Setting:
    """`Setting` is a Python DataClass

    TODO: it seems the Setting class is redudant? why not just using options?
    """
    apk_path: str
    device_serial: str = None
    output_dir:str ="output"
    is_emulator: bool =True     #True for emulators, False for real devices.
    policy_name: str = DEFAULT_POLICY
    random_input: bool =True
    script_path: str=None
    event_interval: int= DEFAULT_EVENT_INTERVAL
    timeout: int = DEFAULT_TIMEOUT
    event_count: int= DEFAULT_EVENT_COUNT
    cv_mode=None
    debug_mode: bool=False
    keep_app:bool=None
    keep_env=None
    profiling_method=None
    grant_perm: bool=True
    send_document: bool=True
    enable_accessibility_hard=None
    master=None
    humanoid=None
    ignore_ad=None
    replay_output=None
    number_of_events_that_restart_app:int =100
    run_initial_rules_after_every_mutation=True
    is_harmonyos:bool=False
    generate_utg:bool=False
    is_package:bool=False

OUTPUT_DIR = "output"

# `d` is the pdl driver for Android or HarmonyOS
d:Union["Android_PDL", "HarmonyOS_PDL", None] = None # TODO move `d` to `kea.py`?

class Kea:
    """
    Kea class
    In Kea, one test case stands for one property file, which includes the elements
    of a property (e.g., the property, the main path, the initializer).
    """
    # the set of all test cases (i.e., all the properties to be tested)
    _all_Kea_PBTests: Dict["Kea", "KeaPBTest"] = {}   
    
    _bundles_: Dict[str, "Bundle"] = {}
    pdl_driver: Optional[Union["Android_PDL", "HarmonyOS_PDL"]]

    @classmethod
    def set_pdl_driver(cls, driver:Optional[Union["Android_PDL", "HarmonyOS_PDL"]]):
        cls.pdl_driver = driver

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.current_rule = None
        self.execute_event = None

    @property
    def all_rules(self) -> List["Rule"]:
        """
        :return: load rules from all Kea_PBTests
        """
        all_rules = []
        for Kea_PBTest in self._all_Kea_PBTests.values():
            all_rules.extend(Kea_PBTest.rule_list)
        return all_rules
    
    @property
    def initializer(self):
        """
        TODO by default, one app only has one initializer
        """
        for kea_test_class_name, Kea_PBTest in self._all_Kea_PBTests.items():
            if len(Kea_PBTest.initializer_list) > 0:
                self.logger.info(f"Successfully found an initializer in {kea_test_class_name}")
                return Kea_PBTest.initializer_list

        self.logger.warning("No initializer found for current apps.")
        return []
    
    @property
    def all_mainPaths(self):
        all_mainPaths = []
        for Kea_PBTest in self._all_Kea_PBTests.values():
            all_mainPaths.extend(Kea_PBTest.mainPath_list)
        return all_mainPaths
    
    @classmethod
    def load_properties(cls, property_files):
        """load the app properties to be tested

        load each property file and instantiate the corresponding test case
        """
        workspace_path = os.path.abspath(os.getcwd())

        # remove duplicates files
        property_files = list(set(property_files))

        for file in property_files:
            
            file_abspath = os.path.join(workspace_path, file) if not os.path.isabs(file) else file
            
            module_dir = os.path.dirname(file_abspath)
            
            # load the module dir into the system path
            if module_dir not in sys.path:
                sys.path.insert(0, module_dir)
            
            if not os.path.exists(file_abspath):
                raise FileNotFoundError(f"{file} not exists.") 
            
            # dynamically change the workspace to make sure 
            # the import of the user properties work correctly
            os.chdir(os.path.dirname(file_abspath))

            module_name, extension_name = [str(_) for _ in os.path.splitext(os.path.basename(file_abspath))]
            if not extension_name == ".py":
                print(f"{file} is not a property file... skipping this file")
                continue
            
            try:
                # print(f"Importting module {module_name}")
                module = importlib.import_module(module_name)

                #! IMPORTANT: set the pdl driver in the modules (the user written properties)
                module.d = cls.pdl_driver

                # Find all kea_test_class in the module and attempt to instantiate them.
                for _, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and issubclass(obj, Kea) and obj is not Kea:
                        print(f"Loading property {obj.__name__} from {file}")
                        Kea.load_Kea_PBTest(obj)

            except ModuleNotFoundError as e:
                print(f"Error importing module {module_name}: {e}")
            
        os.chdir(workspace_path)
    
    @classmethod
    def load_Kea_PBTest(cls, kea_test_class:"Kea"):
        """load Kea_PBTest from kea_test_class and save it to the class var _all_Kea_PBTests

        ### :input:
        kea_test_class: the usr defined test class when writing properties. this should be a child class of class Kea
        """

        current_keaPBTest = cls.init_KeaPBTest(kea_test_class)

        current_keaPBTest.load_initializer_list(kea_test_class)        
        current_keaPBTest.load_rule_list(kea_test_class)
        current_keaPBTest.load_mainPath_list(kea_test_class)

        if len(current_keaPBTest.rule_list) == 0:
            raise Exception(f"No rule defined in {cls.__name__}")
    
    @classmethod
    def init_KeaPBTest(cls, kea_test_class:"Kea") -> "KeaPBTest":
        """
        Init the KeaPBTest for current kea_test_class. 
        If the KeaPBTest for current kea_test_class has already been initialized. Find it and return it.

        :return: KeaPBTest
        """
        # use a dict to store the KeaPBTest obj and make sure every 
        # KeaPBTest obj can only be instantiate once.
        current_Kea_PBTest = cls._all_Kea_PBTests.get(kea_test_class, KeaPBTest())
        cls._all_Kea_PBTests[kea_test_class] = current_Kea_PBTest
        return current_Kea_PBTest
  
    @classmethod
    def set_bundle(cls, type_name):
        bundle = Bundle(type_name)
        cls._bundles_[type_name] = bundle
        return bundle

    def execute_rules(self, rules):
        '''
        random choose a rule, if the rule has preconditions, check the preconditions.
        if the preconditions are satisfied, execute the rule.
        '''
        
        if len(rules) == 0:
            return CHECK_RESULT.PRECON_INVALID
        rule_to_check = random.choice(rules)
        self.current_rule = rule_to_check
        return self.execute_rule(rule_to_check)

    def execute_rule(self, rule:"Rule"):
        """
        execute a rule and return the execution result
        """
        self.logger.info(f"executing rule:\n{rule}")
        if len(rule.preconditions) > 0:
            if not all(precond(self) for precond in rule.preconditions):
                return CHECK_RESULT.PRECON_INVALID
        # try to execute the rule and catch the exception if assertion error throws
        result = CHECK_RESULT.PASS
        try:
            time.sleep(1)
            # execute the interaction scenario I
            result = rule.function(self)
            time.sleep(1)
        except UiObjectNotFoundError as e:

            self.logger.info("Could not find the UI object.")
            import traceback
            tb = traceback.extract_tb(e.__traceback__)
    
            # Find the last traceback information, specifically the error inside rule.function
            last_call = tb[1]
            line_number = last_call.lineno
            file_name = last_call.filename
            code_context = last_call.line.strip()

            # Print the line number and code content of the error.
            self.logger.warning(f"Error occurred in file {file_name} on line {line_number}:")
            self.logger.warning(f"Code causing the error: {code_context}")
            return CHECK_RESULT.UI_NOT_FOUND
        except AssertionError as e:
            # the postcondition Q is violated 
            self.logger.error("Assertion error. "+str(e))
            return CHECK_RESULT.ASSERTION_ERROR
        finally:
            result = CHECK_RESULT.PASS

        return CHECK_RESULT.PASS

    def parse_mainPath(self, mainPath:"MainPath") :
        return mainPath.function, mainPath.path

    def exec_mainPath(self, executable_script):
        # d for PDL driver. Set the d as a local var to make it available in exectuable_scripts
        d = self.pdl_driver
        exec(executable_script)

    def get_rules_whose_preconditions_are_satisfied(self) -> List:
        '''Check all rules and return the list of rules that meet the preconditions.'''
        rules_passed_precondition = []
        for target_rule in self.all_rules:
            if len(target_rule.preconditions) > 0:
                if all(precond(self) for precond in target_rule.preconditions):
                    rules_passed_precondition.append(target_rule)

        return rules_passed_precondition

    def get_rules_without_preconditions(self):
        '''Return the list of rules that do not have preconditions.'''
        rules_without_preconditions = []
        for target_rule in self.all_rules:
            if len(target_rule.preconditions) == 0:
                rules_without_preconditions.append(target_rule)
        return rules_without_preconditions

    def teardown(self):
        """Called after a run has finished executing to clean up any necessary
        state.
        Does nothing by default.
        """
        ...