import logging
import random
from typing import (
    Any,
    Callable,
    Dict,
    List
)
import traceback
import attr
from kea import env_manager, input_manager
from kea.Bundle import Bundle
from kea.droidbot import DroidBot
import inspect
from copy import copy
from uiautomator2.exceptions import UiObjectNotFoundError
import time
from hypothesis.errors import NonInteractiveExampleWarning
import warnings
from dataclasses import dataclass
from kea.utils import SingletonMeta
from typing import TYPE_CHECKING, Union
if TYPE_CHECKING:
    from kea.dsl import Mobile as Android_Mobile
    from kea.dsl_hm import Mobile as HarmonyOS_Mobile

warnings.filterwarnings("ignore", category=NonInteractiveExampleWarning)
import coloredlogs
coloredlogs.install()

RULE_MARKER = "tool_rule"
INITIALIZER_MARKER = "tool_initializer"
PRECONDITIONS_MARKER = "tool_preconditions"
INVARIANT_MARKER = "tool_invariant"
MAINPATH_MARKER = "tool_mainPath"

@attr.s()
class Rule:    # tingsu: what does these mean, including Rule, MainPath, initializer, precondition?
    function = attr.ib()
    preconditions = attr.ib()

    def __str__(self) -> str:
        return f"Rule(function: {self.function.__qualname__})"

@attr.s()
class MainPath:
    function = attr.ib()
    path = attr.ib()

def rule() -> Callable:
    def accept(f):
        precondition = getattr(f, PRECONDITIONS_MARKER, ())
        rule = Rule(function=f, preconditions=precondition)

        def rule_wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        setattr(rule_wrapper, RULE_MARKER, rule)
        return rule_wrapper

    return accept


def precondition(precond: Callable[[Any], bool]) -> Callable:
    def accept(f):
        def precondition_wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        rule = getattr(f, RULE_MARKER, None)
        if rule is not None:
            new_rule = attr.evolve(rule, preconditions=rule.preconditions + (precond,))
            setattr(precondition_wrapper, RULE_MARKER, new_rule)
        else:
            setattr(
                precondition_wrapper,
                PRECONDITIONS_MARKER,
                getattr(f, PRECONDITIONS_MARKER, ()) + (precond,),
            )
        return precondition_wrapper

    return accept


def initializer():
    '''
    An initialize decorator behaves like a rule, but all ``@initialize()`` decorated
    methods will be called before any ``@rule()`` decorated methods, in an arbitrary
    order.  Each ``@initialize()`` method will be called exactly once per run, unless
    one raises an exception.
    '''

    def accept(f):
        def initialize_wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        rule = Rule(function=f, preconditions=())
        setattr(initialize_wrapper, INITIALIZER_MARKER, rule)
        return initialize_wrapper

    return accept

def mainPath():
    def accept(f):
        def mainpath_wrapper(*args, **kwargs):
            source_code = inspect.getsource(f)
            code_lines = [line.strip() for line in source_code.splitlines() if line.strip()]
            code_lines = [line for line in code_lines if not line.startswith('def ') and not line.startswith('@') and not line.startswith('#')]
            return code_lines

        main_path = MainPath(function=f, path=mainpath_wrapper())
        setattr(mainpath_wrapper, MAINPATH_MARKER, main_path)
        return mainpath_wrapper

    return accept

@dataclass
class Setting:
    apk_path: str
    device_serial: str ="emulator-5554"
    output_dir:str ="output"
    is_emulator: bool =True     #True for emulator, false for real device.
    policy_name: str =input_manager.DEFAULT_POLICY
    random_input: bool =True
    script_path: str=None
    event_interval: int=input_manager.DEFAULT_EVENT_INTERVAL
    timeout: int =input_manager.DEFAULT_TIMEOUT
    event_count: int=input_manager.DEFAULT_EVENT_COUNT
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

OUTPUT_DIR = "output"
from .dsl import Mobile
# d:Union["Android_Mobile", "HarmonyOS_Mobile"] | None = Mobile()
d:Union["Android_Mobile", "HarmonyOS_Mobile"] | None = None

def start_kea(kea_core:"Kea", settings:"Setting" = None):
    # if settings is None:
    #     settings = kea_core.TestCase.settings

    droid = DroidBot(    # tingsu: why not naming "droid" as "droidbot"?
        app_path=settings.apk_path,
        device_serial=settings.device_serial,
        is_emulator=settings.is_emulator,
        output_dir=settings.output_dir,
        env_policy=env_manager.POLICY_NONE,
        policy_name=settings.policy_name,
        random_input=settings.random_input,
        script_path=settings.script_path,
        event_interval=settings.event_interval,
        timeout=settings.timeout,
        event_count=settings.event_count,
        cv_mode=settings.cv_mode,
        debug_mode=settings.debug_mode,
        keep_app=settings.keep_app,
        keep_env=settings.keep_env,
        profiling_method=settings.profiling_method,
        grant_perm=settings.grant_perm,
        send_document=settings.send_document,
        enable_accessibility_hard=settings.enable_accessibility_hard,
        master=settings.master,
        humanoid=settings.humanoid,
        ignore_ad=settings.ignore_ad,
        replay_output=settings.replay_output,
        kea_core=kea_core,
        number_of_events_that_restart_app=settings.number_of_events_that_restart_app,
        run_initial_rules_after_every_mutation=settings.run_initial_rules_after_every_mutation,
        is_harmonyos=settings.is_harmonyos
    )

    global d
    d = settings.d

    d.set_device_serial(settings.device_serial)
    d.set_droidbot(droid)
    droid.start()

from hypothesis import strategies as st

class TestCase:   # tingsu: what does TestCase stands for ??

    # TestCase requires a Singleton design to ensure the rule, initializer, mainPath can be correctly loaded
    
    rule_list:List["Rule"]
    initializer_list:List["Rule"]
    mainPath_list:List["MainPath"]

    def get_list(self, MARKER:str, kea_core:"Kea"):
        """
        Dynamically get the rule/initializer/mainPath list from the testCase.
        """

        mapping = {INITIALIZER_MARKER:"initializer_list",
                   MAINPATH_MARKER:"mainPath_list",
                   RULE_MARKER:"rule_list"}
        TARGET_LIST_NAME = mapping[MARKER]

        # return the list if it has already been initialized
        if hasattr(self, TARGET_LIST_NAME):
            return getattr(self, TARGET_LIST_NAME)

        # Else, initialize the list 
        # (TestCase is singleton so the other initialized lists won't be covered)
        setattr(self, TARGET_LIST_NAME, [])
        for _, v in inspect.getmembers(kea_core):
            r = getattr(v, MARKER, None)
            if r is not None:
                getattr(self, TARGET_LIST_NAME).append(r)
        return getattr(self, TARGET_LIST_NAME)



class Kea(object):   # tingsu: what is the purpose of Kea? not very clear. It seems Kea manages the properties
    _all_testCase: Dict[type, "TestCase"] = {}
    _bundles_: Dict[str, Bundle] = {}

    def __init__(self, kea_core: "Kea" = None):
        if kea_core is None:
            self.logger = logging.getLogger(self.__class__.__name__)
            return
        self._initialize_rules_to_run = copy(kea_core.get_initializer_list())
        if not kea_core.get_rule_list():
            raise Exception(f"Type {type(self).__name__} defines no rules")
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
        for testCase in self._all_testCase.values():
            all_rules.extend(testCase.rule_list)
        return all_rules
    
    @property
    def initializer(self):
        for testCaseName, testCase in self._all_testCase.items():
            r = testCase.get_list(INITIALIZER_MARKER, kea_core=self)
            if len(r) > 0:
                self.logger.info(f"Successfully found an initializer in {testCaseName}")
                return r

        self.logger.warning("No initializer found for current apps.")
        return [] 
    
    @classmethod
    def get_initializer_list(cls):
        current_TestCase = cls._all_testCase[cls] = cls._all_testCase.get(cls, TestCase())
        initializer_list = current_TestCase.get_list(INITIALIZER_MARKER, kea_core=cls)
        if len(initializer_list) > 0:
            return initializer_list

    @classmethod
    def get_rule_list(cls):
        current_TestCase = cls._all_testCase[cls] = cls._all_testCase.get(cls, TestCase())
        rule_list = current_TestCase.get_list(RULE_MARKER, kea_core=cls)
        return rule_list

    @classmethod
    def get_mainPath_list(cls):
        current_TestCase = cls._all_testCase[cls] = cls._all_testCase.get(cls, TestCase())
        mainPath_list = current_TestCase.get_list(MAINPATH_MARKER, kea_core=cls)
        return mainPath_list

    @classmethod
    def set_bundle(cls, type_name):
        bundle = Bundle(type_name)
        cls._bundles_[type_name] = bundle
        return bundle

    def execute_initializers(self):
        for initializer in self._initialize_rules_to_run:
            initializer.function(self)

    def execute_rules(self, rules):
        '''random choose a rule, if the rule has preconditions, check the preconditions.
        if the preconditions are satisfied, execute the rule.'''
        '''

        0: assertion error
        1: check property pass
        2: UiObjectNotFoundError
        3: don't need to check property,because the precondition is not satisfied
        '''
        
        if len(rules) == 0:
            return 3
        rule_to_check = random.choice(rules)
        self.current_rule = rule_to_check
        return self.execute_rule(rule_to_check)

    def execute_rule(self, rule:"Rule"):
        self.logger.info(f"executing rule:\n{rule}")
        if len(rule.preconditions) > 0:
            if not all(precond(self) for precond in rule.preconditions):
                return 3
        # try to execute the rule and catch the exception if assertion error throws
        result = 1
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
            return 2
        except AssertionError as e:
            self.logger.error("Assertion error. "+str(e))
            return 0
        finally:
            result = 1

        return result

    def get_mainPath(self, mainPath:"MainPath") :
        return mainPath.function, mainPath.path

    def exec_mainPath(self, event_str):
        exec(event_str)

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