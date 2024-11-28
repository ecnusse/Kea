from dataclasses import dataclass
import traceback
import logging
import random
import time
from typing import Dict, List, TYPE_CHECKING, Optional, Union
from .testcase import TestCase
from kea.Bundle import Bundle
from uiautomator2.exceptions import UiObjectNotFoundError

if TYPE_CHECKING:
    from .testcase import Rule, MainPath
    from .pdl import PDL as Android_PDL
    from .pdl_hm import PDL as HarmonyOS_PDL

from .utils import INITIALIZER_MARKER, RULE_MARKER, MAINPATH_MARKER

@dataclass
class CHECK_RESULT:
    ASSERTION_ERROR = 0
    PASS = 1
    UI_NOT_FOUND = 2
    PRECON_INVALID = 3

class Kea:
    _all_testCases: Dict[type, "TestCase"] = {}
    _bundles_: Dict[str, "Bundle"] = {}
    d: Optional[Union["Android_PDL", "HarmonyOS_PDL"]]

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.current_rule = None
        self.execute_event = None

    def start(self):
        try:
            self.droidbot.start()
        except Exception:
            traceback.print_exc()

    @property
    def all_rules(self) -> List["Rule"]:
        """
        :return: load rules from all the provided testCases 
        """
        all_rules = []
        for testCase in self._all_testCases.values():
            all_rules.extend(testCase.rule_list)
        return all_rules
    
    @property
    def initializer(self):
        for testCaseName, testCase in self._all_testCases.items():
            r = testCase.get_list(INITIALIZER_MARKER, kea=self)
            if len(r) > 0:
                self.logger.info(f"Successfully found an initializer in {testCaseName}")
                return r

        self.logger.warning("No initializer found for current apps.")
        return []
    
    @property
    def all_mainPaths(self):
        all_mainPaths = []
        for testCase in self._all_testCases.values():
            all_mainPaths.extend(testCase.mainPath_list)
        return all_mainPaths
    
    @classmethod
    def load_testCase(cls, test_case:"Kea"):
        test_case.load_initializer_list()
        test_case.load_mainPath_list()
        test_case.load_rule_list()

        if not test_case.load_rule_list():
            raise Exception(f"Type {type(test_case).__name__} defines no rules")
    
    @classmethod
    def load_initializer_list(cls):
        current_TestCase = cls._all_testCases[cls] = cls._all_testCases.get(cls, TestCase())
        initializer_list = current_TestCase.get_list(INITIALIZER_MARKER, kea=cls)
        if len(initializer_list) > 0:
            return initializer_list

    @classmethod
    def load_rule_list(cls):
        current_TestCase = cls._all_testCases[cls] = cls._all_testCases.get(cls, TestCase())
        rule_list = current_TestCase.get_list(RULE_MARKER, kea=cls)
        return rule_list

    @classmethod
    def load_mainPath_list(cls):
        current_TestCase = cls._all_testCases[cls] = cls._all_testCases.get(cls, TestCase())
        mainPath_list = current_TestCase.get_list(MAINPATH_MARKER, kea=cls)
        return mainPath_list

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
        self.logger.info(f"executing rule:\n{rule}")
        if len(rule.preconditions) > 0:
            if not all(precond(self) for precond in rule.preconditions):
                return CHECK_RESULT.PRECON_INVALID
        # try to execute the rule and catch the exception if assertion error throws
        result = CHECK_RESULT.PASS
        try:
            time.sleep(1)
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
            self.logger.error("Assertion error. "+str(e))
            return CHECK_RESULT.ASSERTION_ERROR
        finally:
            result = CHECK_RESULT.PASS

        return CHECK_RESULT.PASS

    def parse_mainPath(self, mainPath:"MainPath") :
        return mainPath.function, mainPath.path

    def exec_mainPath(self, executable_script):
        # d for DSL object. Set the d as a local var to make it available in exectuable_scripts
        d = self.d
        exec(executable_script)

    def get_rules_that_pass_the_preconditions(self) -> List:
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