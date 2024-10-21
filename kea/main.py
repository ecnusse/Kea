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
import uiautomator2 as u2
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
from kea.dsl import Mobile
warnings.filterwarnings("ignore", category=NonInteractiveExampleWarning)

RULE_MARKER = "tool_rule"
INITIALIZE_RULE_MARKER = "tool_initialize_rule"
PRECONDITIONS_MARKER = "tool_preconditions"
INVARIANT_MARKER = "tool_invariant"
MAINPATH_MARKER = "tool_main_path"

@attr.s()
class Rule:
    function = attr.ib()
    preconditions = attr.ib()

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


def initialize():
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
        setattr(initialize_wrapper, INITIALIZE_RULE_MARKER, rule)
        return initialize_wrapper

    return accept

def main_path():
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

OUTPUT_DIR = "output"
d = Mobile()

def run_android_check_as_test(android_check_class, settings = None):
    if settings is None:
        settings = android_check_class.TestCase.settings

    def run_android_check(android_check_class):

        droid = DroidBot(
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
            android_check=android_check_class,
            number_of_events_that_restart_app=settings.number_of_events_that_restart_app,
            run_initial_rules_after_every_mutation=settings.run_initial_rules_after_every_mutation
        )
        global d
        d.set_device_serial(settings.device_serial)
        d.set_droidbot(droid)
        droid.start()
    run_android_check(android_check_class)
from hypothesis import strategies as st
class Kea(object):
    _rules_per_class: Dict[type, List[classmethod]] = {}
    _initializers_per_class: Dict[type, List[classmethod]] = {}
    _main_path_per_class: Dict[type, List[classmethod]] = {}
    _bundles_: Dict[str, Bundle] = {}

    def __init__(
        self
    ):
        self._initialize_rules_to_run = copy(self.initialize_rules())
        if not self.rules():
            raise Exception(f"Type {type(self).__name__} defines no rules")
        self.current_rule = None
        self.execute_event = None
        self.logger = logging.getLogger(self.__class__.__name__)

    def start(self):
        try:
            self.droidbot.start()
        except Exception:
            traceback.print_exc()

    @classmethod
    def initialize_rules(cls):
        try:
            return cls._initializers_per_class[cls]
        except KeyError:
            pass
        cls._initializers_per_class[cls] = []
        for _, v in inspect.getmembers(cls):
            r = getattr(v, INITIALIZE_RULE_MARKER, None)
            if r is not None:
                cls._initializers_per_class[cls].append(r)
        return cls._initializers_per_class[cls]

    @classmethod
    def rules(cls):
        try:
            return cls._rules_per_class[cls]
        except KeyError:
            pass

        cls._rules_per_class[cls] = []
        for _, v in inspect.getmembers(cls):
            r = getattr(v, RULE_MARKER, None)
            if r is not None:
                cls._rules_per_class[cls].append(r)
        return cls._rules_per_class[cls]

    @classmethod
    def mainpath_lists(cls):
        try:
            return cls._main_path_per_class[cls]
        except KeyError:
            pass

        cls._main_path_per_class[cls] = []
        for _, v in inspect.getmembers(cls):
            r = getattr(v, MAINPATH_MARKER, None)
            if r is not None:
                cls._main_path_per_class[cls].append(r)
        return cls._main_path_per_class[cls]

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

    def execute_rule(self, rule):
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
            self.logger.info(f"Error occurred in file {file_name} on line {line_number}:")
            self.logger.info(f"Code causing the error: {code_context}")
            return 2
        except AssertionError as e:
            self.logger.error("Assertion error. "+str(e))
            return 0
        finally:
            result = 1

        return result

    def get_main_path(self, mainpath) :
        return mainpath.function, mainpath.path

    def exec_main_path(self, event_str):
        exec(event_str)

    def get_rules_that_pass_the_preconditions(self) -> List:
        '''Check all rules and return the list of rules that meet the preconditions.'''
        rules_to_check = self.rules()
        rules_meeting_preconditions = []
        for class_name in self._rules_per_class:
            rules_to_check = self._rules_per_class[class_name]
            for rule_to_check in rules_to_check:
                if len(rule_to_check.preconditions) > 0:
                    if all(precond(self) for precond in rule_to_check.preconditions):
                        rules_meeting_preconditions.append(rule_to_check)
        return rules_meeting_preconditions

    def get_rules_without_preconditions(self):
        '''Return the list of rules that do not have preconditions.'''
        rules_to_check = self.rules()
        rules_without_preconditions = []
        for class_name in self._rules_per_class:
            rules_to_check = self._rules_per_class[class_name]
            for rule_to_check in rules_to_check:
                if len(rule_to_check.preconditions) == 0:
                    rules_without_preconditions.append(rule_to_check)
        return rules_without_preconditions

    def teardown(self):
        """Called after a run has finished executing to clean up any necessary
        state.
        Does nothing by default.
        """
        ...