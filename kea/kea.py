import logging
import random
import time
import os
import sys
import importlib
import inspect
import attr
from .utils import INITIALIZER_MARKER, MAINPATH_MARKER, RULE_MARKER

from dataclasses import dataclass
from typing import Dict, List, TYPE_CHECKING, Optional, Union
from uiautomator2.exceptions import UiObjectNotFoundError

if TYPE_CHECKING:
    from .kea_test import Rule, MainPath, KeaTest
    from .android_pdl_driver import Android_PDL_Driver
    from .harmonyos_pdl_driver import HarmonyOS_PDL_Driver

@dataclass
class CHECK_RESULT:
    ASSERTION_FAILURE = 0
    PASS = 1
    UI_NOT_FOUND = 2
    PRECON_NOT_SATISFIED = 3
    UNKNOWN_EXECPTION = 4

OUTPUT_DIR = "output"

@attr.s(frozen=True)
class Rule:    
    """
    A rule corresponds to a property, including the preconditions, 
    the interaction scenario, the postconditions (in the form of assertions).
    """
    
    # `preconditions` denotes the preconditions annotated with `@precondition`
    preconditions = attr.ib()  

    # `function` denotes the function of @Rule. 
    # This function includes the interaction scenario and the assertions (i.e., the postconditions)
    function = attr.ib()

    def evolve(self, **changes) -> "Rule":
        return Rule(**{**self.__dict__, **changes})

    def __str__(self) -> str:
        r = f"{self.function.__module__}.{self.function.__qualname__.split('.')[0]}.Rule(function: {self.function.__name__})"
        return r

@attr.s()
class Initializer:
  
    # `function` denotes the function of `@initializer.
    function = attr.ib()

@attr.s()
class MainPath:
    
    # `function` denotes the function of `@mainPath.
    function = attr.ib()

    # the interaction steps (events) in the main path
    path: List[str] = attr.ib()  


class KeaTestElements:
    """
    
    KeaTestElements cannot be accessed by the users to avoid information leakage.
    """
    def __init__(self, keaTest_name):
        self.keaTest_name = keaTest_name 
        self.rules:List["Rule"] = list()
        self.initializers:List["Initializer"] = list() # TODO why  "Rule"?
        self.mainPaths:List["MainPath"] = list()

    def load_rules(self, keaTest:"KeaTest"):
        """
        Load the rule from the KeaTest class (user written property).
        """
        for _, v in inspect.getmembers(keaTest):
            rule = getattr(v, RULE_MARKER, None)
            if rule is not None:
                self.rules.append(rule)

    def load_initializers(self, keaTest:"KeaTest"):
        """
        Load the rule from the KeaTest class (user written property).
        """
        for _, v in inspect.getmembers(keaTest):
            initializer = getattr(v, INITIALIZER_MARKER, None)
            if initializer is not None:
                self.initializers.append(initializer)

    def load_mainPaths(self, keaTest:"KeaTest"):
        """
        Load the rule from the KeaTest class (user written property).
        """
        for _, v in inspect.getmembers(keaTest):
            mainPath = getattr(v, MAINPATH_MARKER, None)
            if mainPath is not None:
                self.mainPaths.append(mainPath)

class Kea:
    """Kea class

    Kea class is a manager of all the user defined app properties. It manages all the 
    properties at runtime and provides a set of methods for reading and executing these properties.

    In Kea, one kea test denotes one app property file, which includes the elements
    of a property (i.e., the property, the main path, the initializer).
    """
    # the database storing all kea tests (i.e., all the app properties to be tested)
    _KeaTest_DB: Dict["KeaTest", "KeaTestElements"] = {}
    # the driver for executing kea tests
    _pdl_driver: Optional[Union["Android_PDL_Driver", "HarmonyOS_PDL_Driver"]]
    _all_rules_list = None

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @property
    def all_rules(self) -> List["Rule"]:
        """
        :return: load rules from all Kea_Tests
        """
        if self._all_rules_list is None:
            self._all_rules_list = list()
            for keaTestElements in self._KeaTest_DB.values():
                self._all_rules_list.extend(keaTestElements.rules)
        return self._all_rules_list
    
    @property
    def initializer(self) -> Initializer:
        """
        TODO by default, one app only has one initializer 
        """
        for keaTest, keaTestElements in self._KeaTest_DB.items():
            if len(keaTestElements.initializers) > 0:
                self.logger.info(f"Successfully found an initializer in {keaTest}")
                return keaTestElements.initializers[0]

        self.logger.warning("No initializer found for current apps.")
        return None
    
    @property
    def all_mainPaths(self):
        all_mainPaths = []
        for keaTestElements in self._KeaTest_DB.values():
            all_mainPaths.extend(keaTestElements.mainPaths)
        return all_mainPaths
    
    @classmethod
    def set_pdl_driver(cls, driver:Optional[Union["Android_PDL_Driver", "HarmonyOS_PDL_Driver"]]):
        """set the driver
        """
        cls._pdl_driver = driver
    
    @classmethod
    def load_app_properties(cls, property_files):
        """load the app properties to be tested

        load each property file and instantiate the corresponding test case
        """
        workspace_path = os.path.abspath(os.getcwd())

        # remove duplicated property files
        property_files = list(set(property_files))

        for file in property_files:
            
            # get the absolute path of the property file
            file_abspath = os.path.join(workspace_path, file) if not os.path.isabs(file) else file
            if not os.path.exists(file_abspath):
                raise FileNotFoundError(f"{file} not exists.") 
            
            module_dir = os.path.dirname(file_abspath)
            
            # load the module dir into the system path
            if module_dir not in sys.path:
                sys.path.insert(0, module_dir)
            
            # dynamically change the workspace to make sure 
            # the import of the user properties work correctly
            os.chdir(module_dir)

            # TODO why it is a list [...]
            module_name, extension_name = [str(_) for _ in os.path.splitext(os.path.basename(file_abspath))]
            if not extension_name == ".py":
                print(f"{file} is not a property file... skipping this file")
                continue
            
            try:
                # print(f"Importting module {module_name}")
                module = importlib.import_module(module_name)

                #! IMPORTANT: set the pdl driver in the modules (the user written properties)
                module.d = cls._pdl_driver

                from .kea_test import KeaTest

                # find all kea tests in the module and attempt to instantiate them.
                for _, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and issubclass(obj, KeaTest) and obj is not KeaTest:
                        print(f"Loading property {obj.__name__} from {file}")
                        cls.load_KeaTest(obj)

            except ModuleNotFoundError as e:
                print(f"Error importing module {module_name}: {e}")
            
        os.chdir(workspace_path)
    
    @classmethod
    def load_KeaTest(cls, keaTest:"KeaTest"):
        """load kea tests from the app properties

        """
        keaTestElements = cls.init_KeaTestElements(keaTest)
        keaTestElements.load_initializers(keaTest)        
        keaTestElements.load_rules(keaTest)
        keaTestElements.load_mainPaths(keaTest)

        if len(keaTestElements.rules) == 0:
            raise Exception(f"No rule defined in {cls.__name__}")
    
    @classmethod
    def init_KeaTestElements(cls, keaTest:"KeaTest") -> "KeaTestElements":
        """
        Init the KeaTestElements for current KeaTest.
        If the KeaTestElements for current KeaTest class has already been initialized. Find it and return it.

        :return: KeaPBTest
        """
        # use a dict to store the KeaTestElements obj and make sure every
        # KeaTestElements obj can only be instantiate once.
        keaTest_name = keaTest.__module__ + '.' + keaTest.__name__
        keaTestElements = cls._KeaTest_DB.get(keaTest, KeaTestElements(keaTest_name))
        cls._KeaTest_DB[keaTest] = keaTestElements
        return keaTestElements 

    def execute_rules(self, rules):
        '''
        random choose a rule, if the rule has preconditions, check the preconditions.
        if the preconditions are satisfied, execute the rule.
        '''
        
        if len(rules) == 0:
            return CHECK_RESULT.PRECON_NOT_SATISFIED
        rule_to_check = random.choice(rules)
        return self.execute_rule(rule_to_check, keaTest=None)

    def execute_rule(self, rule:"Rule", keaTest:"KeaTest"):
        """
        execute a rule and return the execution result
        """
        self.logger.info(f"executing rule:\n{rule}")
        if len(rule.preconditions) > 0:
            if not all(precond(keaTest) for precond in rule.preconditions):
                return CHECK_RESULT.PRECON_NOT_SATISFIED
        # try to execute the rule and catch the exception if assertion error throws
        try:
            time.sleep(1)
            # execute the interaction scenario I
            rule.function(keaTest)
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
            self.logger.error("Assertion failed: " + str(e))
            return CHECK_RESULT.ASSERTION_FAILURE
        except Exception as e:
            self.logger.error("Unexpected exeception during executing rule: "+str(e))
            return CHECK_RESULT.UNKNOWN_EXECPTION

        return CHECK_RESULT.PASS

    def execute_initializer(self, initializer: "Initializer"):
        try:
            initializer.function(self)
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
        except Exception as e:
            self.logger.error("Unexpected exeception during executing rule: "+str(e))
            return CHECK_RESULT.UNKNOWN_EXECPTION
        return CHECK_RESULT.PASS

    def execute_event_from_main_path(self, executable_script):
        # d for PDL driver. Set the d as a local var to make it available in exectuable_scripts
        d = self._pdl_driver
        exec(executable_script)

    def get_rules_whose_preconditions_are_satisfied(self) -> Dict["Rule", "KeaTest"]:
        '''Check all rules and return the list of rules that meet the preconditions.'''
        rules_passed_precondition:Dict["Rule", "KeaTest"] = {}
        
        for keaTest, keaTestElements in self._KeaTest_DB.items():
            for target_rule in keaTestElements.rules:
                if len(target_rule.preconditions) > 0:
                    if all(precond(keaTest) for precond in target_rule.preconditions):
                        rules_passed_precondition[target_rule] = keaTest

        return rules_passed_precondition

    def get_rules_without_preconditions(self) -> Dict["Rule", "KeaTest"]:
        '''Return the list of rules that do not have preconditions.
        
           When a rule does not have preconditions, its preconditions are always true
        '''
        rules_without_precondition:Dict["Rule", "KeaTest"] = {}
        
        for keaTest, keaTestElements in self._KeaTest_DB.items():
            for target_rule in keaTestElements.rules:
                if len(target_rule.preconditions) == 0:
                    rules_without_precondition[target_rule] = keaTest
        return rules_without_precondition

    def teardown(self):
        """Called after a run has finished executing to clean up any necessary
        state.
        Does nothing by default.
        """
        ...

