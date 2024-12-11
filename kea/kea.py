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
from typing import Dict, List, TYPE_CHECKING, Optional, Union, Callable
from uiautomator2.exceptions import UiObjectNotFoundError

if TYPE_CHECKING:
    #from .kea_test import Rule, MainPath, KeaTest
    from .pdl import PDL as Android_PDL
    from .pdl_hm import PDL as HarmonyOS_PDL

@dataclass
class CHECK_RESULT:
    ASSERTION_FAILURE = 0
    PASS = 1
    UI_NOT_FOUND = 2
    PRECON_NOT_SATISFIED = 3
    UNKNOWN_EXECPTION = 4

OUTPUT_DIR = "output"

@attr.s(frozen=True)
class Rule:    # tingsu: what does these mean, including Rule, MainPath, initializer, precondition?
    """
    A rule corresponds to a property (including precondition, interaction scenario, postconditions)
    """
    
    # `preconditions` denotes the preconditions annotated with `@precondition`
    preconditions = attr.ib()  # TODO rename `preconditions` to `precondition`?

    # `function` denotes the function of @Rule. This function includes the interaction scenario and the assertions (i.e., the postconditions) therein
    # TODO we may need to rename `function` to `method`?
    function = attr.ib()

    def evolve(self, **changes) -> "Rule":
        return Rule(**{**self.__dict__, **changes})

    def __str__(self) -> str:
        r = f"{self.function.__module__}.{self.function.__qualname__.split('.')[0]}.Rule(function: {self.function.__name__})"
        return r

@attr.s()
class Initializer:
    # TODO - xixian add this class to decorator and modify the typing
    # `function` denotes the function of `@mainPath.
    function = attr.ib()

@attr.s()
class MainPath:
    
    # `function` denotes the function of `@mainPath.
    function = attr.ib()

    # the interaction steps in the main path
    path: List[str] = attr.ib()  # TODO rename `path` to a more suitable name?


class KeaTestElements:
    """
    
    """
    def __init__(self, keaTest_name):
        self.keaTest_name = keaTest_name
        self.rule_list:List["Rule"] = list()
        self.initializer_list:List["Initializer"] = list() # TODO why  "Rule"?
        self.mainPath_list:List["MainPath"] = list()

    def load_rule_list(self, kea_test_class:"KeaTest"):
        """
        Load the rule from the kea_test_class (user written property).
        """
        for _, v in inspect.getmembers(kea_test_class):
            rule = getattr(v, RULE_MARKER, None)
            if rule is not None:
                self.rule_list.append(rule)

    def load_initializer_list(self, kea_test_class:"KeaTest"):
        """
        Load the rule from the kea_test_class (user written property).
        """
        for _, v in inspect.getmembers(kea_test_class):
            initializer = getattr(v, INITIALIZER_MARKER, None)
            if initializer is not None:
                self.initializer_list.append(initializer)

    def load_mainPath_list(self, kea_test_class:"KeaTest"):
        """
        Load the rule from the kea_test_class (user written property).
        """
        for _, v in inspect.getmembers(kea_test_class):
            mainPath = getattr(v, MAINPATH_MARKER, None)
            if mainPath is not None:
                self.mainPath_list.append(mainPath)

class Kea:
    """## Kea class

    Kea class is a manager of all the user defined properties. Which store all the properties
    in runtime and provide a set of methods for reading and executing these properties.
    In Kea, one test case stands for one property file, which includes the elements
    of a property (e.g., the property, the main path, the initializer).
    """
    # the set of all test cases (i.e., all the properties to be tested)

    _KeaTest_DB: Dict["KeaTest", "KeaTestElements"] = {}
    _pdl_driver: Optional[Union["Android_PDL", "HarmonyOS_PDL"]]
    _all_rules_list = None

    @classmethod
    def set_pdl_driver(cls, driver:Optional[Union["Android_PDL", "HarmonyOS_PDL"]]):
        cls._pdl_driver = driver

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @property
    def all_rules(self) -> List["Rule"]:
        """
        :return: load rules from all Kea_PBTests
        """
        if self._all_rules_list is None:
            self._all_rules_list = list()
            for keaTestElements in self._KeaTest_DB.values():
                self._all_rules_list.extend(keaTestElements.rule_list)
        return self._all_rules_list
    
    @property
    def initializer(self) -> Initializer:
        """
        TODO by default, one app only has one initializer 
        """
        for keaTest, keaTestElements in self._KeaTest_DB.items():
            if len(keaTestElements.initializer_list) > 0:
                self.logger.info(f"Successfully found an initializer in {keaTest}")
                return keaTestElements.initializer_list[0]

        self.logger.warning("No initializer found for current apps.")
        return None
    
    @property
    def all_mainPaths(self):
        all_mainPaths = []
        for keaTestElements in self._KeaTest_DB.values():
            all_mainPaths.extend(keaTestElements.mainPath_list)
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
                module.d = cls._pdl_driver

                from .kea_test import KeaTest

                # Find all kea_test_class in the module and attempt to instantiate them.
                for _, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and issubclass(obj, KeaTest) and obj is not KeaTest:
                        print(f"Loading property {obj.__name__} from {file}")
                        cls.load_KeaTest(obj)

            except ModuleNotFoundError as e:
                print(f"Error importing module {module_name}: {e}")
            
        os.chdir(workspace_path)
    
    @classmethod
    def load_KeaTest(cls, keaTest:"KeaTest"):
        """load Kea_PBTest from kea_test_class and save it to the class var _all_Kea_PBTests

        ### :input:
        kea_test_class: the usr defined test class when writing properties. this should be a child class of class Kea
        """

        current_keaTestElements = cls.init_KeaTestElements(keaTest)

        current_keaTestElements.load_initializer_list(keaTest)        
        current_keaTestElements.load_rule_list(keaTest)
        current_keaTestElements.load_mainPath_list(keaTest)

        if len(current_keaTestElements.rule_list) == 0:
            raise Exception(f"No rule defined in {cls.__name__}")
    
    @classmethod
    def init_KeaTestElements(cls, keaTest:"KeaTest") -> "KeaTestElements":
        """
        Init the KeaPBTest for current kea_test_class. 
        If the KeaPBTest for current kea_test_class has already been initialized. Find it and return it.

        :return: KeaPBTest
        """
        # use a dict to store the KeaPBTest obj and make sure every 
        # KeaPBTest obj can only be instantiate once.
        keaTest_name = keaTest.__module__ + '.' + keaTest.__name__
        current_keaTestElements = cls._KeaTest_DB.get(keaTest, KeaTestElements(keaTest_name))
        cls._KeaTest_DB[keaTest] = current_keaTestElements
        return current_keaTestElements 

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

    def exec_mainPath(self, executable_script):
        # d for PDL driver. Set the d as a local var to make it available in exectuable_scripts
        d = self._pdl_driver
        exec(executable_script)

    def get_rules_whose_preconditions_are_satisfied(self) -> Dict["Rule", "KeaTest"]:
        '''Check all rules and return the list of rules that meet the preconditions.'''
        # rules_passed_precondition = []
        rules_passed_precondition:Dict["Rule", "KeaTest"] = {}
        
        for keaTest, keaTestElements in self._KeaTest_DB.items():
            for target_rule in keaTestElements.rule_list:
                if len(target_rule.preconditions) > 0:
                    if all(precond(keaTest) for precond in target_rule.preconditions):
                        rules_passed_precondition[target_rule] = keaTest

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

