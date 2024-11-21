from dataclasses import dataclass
import os

import logging
import random
import copy
import time

from .utils import Time
from abc import abstractmethod
from .input_event import (
    KEY_RotateDeviceNeutralEvent,
    KEY_RotateDeviceRightEvent,
    KeyEvent,
    IntentEvent,
    ReInstallAppEvent,
    RotateDevice,
    RotateDeviceNeutralEvent,
    RotateDeviceRightEvent,
    KillAppEvent,
    KillAndRestartAppEvent,
    U2StartEvent
)
from .utg import UTG
from kea import utils
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .input_manager import InputManager
    from .main import Kea
    from .app import App
    from .device import Device

# Max number of restarts
MAX_NUM_RESTARTS = 5
# Max number of steps outside the app
MAX_NUM_STEPS_OUTSIDE = 10
MAX_NUM_STEPS_OUTSIDE_KILL = 10
# Max number of replay tries
MAX_REPLY_TRIES = 5
ACTION_COUNT_TO_START = 2

# Some input event flags
EVENT_FLAG_STARTED = "+started"
EVENT_FLAG_START_APP = "+start_app"
EVENT_FLAG_STOP_APP = "+stop_app"
EVENT_FLAG_EXPLORE = "+explore"
EVENT_FLAG_NAVIGATE = "+navigate"
EVENT_FLAG_TOUCH = "+touch"

# Policy taxanomy
POLICY_GUIDED = "guided"
POLICY_RANDOM = "random"
POLICY_NONE = "none"


@dataclass
class RULE_STATE:
    SATISFY_PRE = "#satisfy pre"
    CHECK_PROPERTY = "#check property"
    TRIGGER_BUG = "#trigger the bug"

@dataclass
class CHECK_RESULT:
    ASSERTION_ERROR = 0
    PASS = 1
    UI_NOT_FOUND = 2
    PRECON_NOT_SATISFIED = 3


class InputInterruptedException(Exception):
    pass


class InputPolicy(object):
    """
    This class is responsible for generating events to stimulate more app behaviour
    It should call AppEventManager.send_event method continuously
    """

    def __init__(self, device:"Device", app:"App", kea_core:"Kea"=None):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.time_recoder = Time()

        self.device = device
        self.app = app
        self.action_count = 0
        self.master = None
        self.kea_core = kea_core
        self.input_manager = None
        self.time_needed_to_satisfy_precondition = []

        self.time_to_check_rule = []

        self.last_event = None

    def run_initial_rules(self):
        if len(self.kea_core.initializer) == 0:
            self.logger.warning("No initializer")
            return
        

        result = self.kea_core.execute_rules(self.kea_core.initializer)
        if result:
            self.logger.info("-------initialize successfully-----------")
        else:
            self.logger.error("-------initialize failed-----------")

    def start(self, input_manager:"InputManager"):
        """
        start producing events
        :param input_manager: instance of InputManager
        """
        self.action_count = 0
        self.input_manager = input_manager
        while (
                input_manager.enabled
                and self.action_count
                < input_manager.event_count
        ):
            try:
                # TODO refactor this code. set ime when using android
                if hasattr(self.device, "u2"):
                    self.device.u2.set_fastinput_ime(True)
                self.logger.info("action count: %d" % self.action_count)
                if self.action_count == 0 and self.master is None:
                    #If the application is running, close the application.
                    event = KillAppEvent(app=self.app)
                elif self.action_count == 1 and self.master is None:
                    event = IntentEvent(self.app.get_start_intent())
                else:
                    event = self.generate_event()
                self.last_event = event
                input_manager.add_event(event)
            except KeyboardInterrupt:
                break
            except InputInterruptedException as e:
                self.logger.info("stop sending events: %s" % e)
                self.logger.info("action count: %d" % self.action_count)
                break

            except RuntimeError as e:
                self.logger.info("RuntimeError: %s, stop sending events" % e)
                break
            except Exception as e:
                self.logger.warning("exception during sending events: %s" % e)
                import traceback

                traceback.print_exc()
            self.action_count += 1
        self.tear_down()

    @abstractmethod
    def tear_down(self):
        """
        
        """
        pass

    @abstractmethod
    def generate_event(self):
        """
        generate an event
        @return:
        """
        pass

    @abstractmethod
    def generate_explore_event(self):
        """
        generate an event
        @return:
        """
        pass


class KeaInputPolicy(InputPolicy):
    """
    state-based input policy
    """

    def __init__(self, device, app, random_input, kea_core=None):
        super(KeaInputPolicy, self).__init__(device, app, kea_core)
        self.random_input = random_input
        self.script = None
        self.master = None
        self.script_events = []
        self.last_event = None
        self.last_state = None
        self.current_state = None
        self.utg = UTG(
            device=device, app=app, random_input=random_input
        )
        self.script_event_idx = 0
        if self.device.humanoid is not None:
            self.humanoid_view_trees = []
            self.humanoid_events = []
        
        # retrive all the rules from the provided properties
        self.rules = {}
        for rule in self.kea_core.all_rules:
            self.rules[rule.function.__name__] = {RULE_STATE.SATISFY_PRE: 0, RULE_STATE.CHECK_PROPERTY: 0, RULE_STATE.TRIGGER_BUG: 0}
        # record the action count, time and property name when the bug is triggered
        self.triggered_bug_information = []

    def check_rule_with_precondition(self):
        rules_to_check = self.kea_core.get_rules_that_pass_the_preconditions()
        if len(rules_to_check) == 0:
            self.logger.debug("No rules match the precondition")
            if hasattr(self, "not_reach_precondition_path_number"):
                self.not_reach_precondition_path_number.append(self.path_index)
            return
            # continue

        for rule in rules_to_check:
            self.rules[rule.function.__name__][RULE_STATE.SATISFY_PRE] += 1
        rule_to_check = random.choice(rules_to_check)

        if rule_to_check is not None:
            self.logger.info("-------check rule : %s------" % rule_to_check)
            self.rules[rule_to_check.function.__name__][RULE_STATE.CHECK_PROPERTY] += 1

            # check rule, record relavant info and output log
            result = self.kea_core.execute_rule(rule_to_check)
            if result == CHECK_RESULT.ASSERTION_ERROR:
                self.logger.error("-------check rule : assertion error------")
                self.logger.debug("-------time from start : %s-----------" % str(self.time_recoder.get_time_duration()))
                self.rules[rule_to_check.function.__name__][RULE_STATE.TRIGGER_BUG] += 1
                self.triggered_bug_information.append(
                    (self.action_count, self.time_recoder.get_time_duration(), rule_to_check.function.__name__))


            elif result == CHECK_RESULT.PASS:
                self.logger.info("-------check rule : pass------")
                self.logger.debug("-------time from start : %s-----------" % str(self.time_recoder.get_time_duration()))

            elif result == CHECK_RESULT.UI_NOT_FOUND:
                self.logger.error("-------rule execute failed: UiObjectNotFoundError-----------")

            elif result == CHECK_RESULT.PRECON_NOT_SATISFIED:
                self.logger.info("-------precondition is not satisfied-----------")
            
            else:
                raise AttributeError(f"invalid check rule result {result}")

    def check_rule_without_precondition(self):
        rules_to_check = self.kea_core.get_rules_without_preconditions()
        if len(rules_to_check) > 0:
            result = self.kea_core.execute_rules(
                self.kea_core.get_rules_without_preconditions()
            )
            if result:
                self.logger.info("-------rule_without_precondition execute success-----------")
            else:
                self.logger.error("-------rule_without_precondition execute failed-----------")
        else:
            self.logger.info("-------no rule_without_precondition to execute-----------")

    def stop_app_events(self):
        # self.logger.info("reach the target state, restart the app")
        stop_app_intent = self.app.get_stop_intent()
        stop_event = IntentEvent(stop_app_intent)
        self.logger.info("stop the app and go back to the main activity")
        return stop_event

    def generate_event(self):
        """
        generate an event
        @return:
        """
        pass

    def update_utg(self):
        self.utg.add_transition(self.last_event, self.last_state, self.current_state)

    def update_node(self, event, state):
        self.utg.add_node(state, event)

    @abstractmethod
    def generate_event_based_on_utg(self):
        """
        generate an event based on UTG
        :return: InputEvent
        """
        pass

    def tear_down(self):
        """
        
        """
        # mark the bug information on the bug report html
        if len(self.triggered_bug_information) > 0:
            bug_report_path = os.path.join(self.device.output_dir, "all_states")
            utils.generate_report(
                bug_report_path,
                self.device.output_dir,
                self.triggered_bug_information
            )
        self.logger.info("----------------------------------------")

        if len(self.triggered_bug_information) > 0:
            self.logger.info("the first time needed to trigger the bug: %s" % self.triggered_bug_information[0][1])

        if len(self.time_needed_to_satisfy_precondition) > 0:
            self.logger.info(
                "the first time needed to satisfy the precondition: %s" % self.time_needed_to_satisfy_precondition[0])
            self.logger.info(
                "How many times satisfy the precondition: %s" % len(self.time_needed_to_satisfy_precondition))
            if len(self.triggered_bug_information) > 0:
                self.logger.info("How many times trigger the bug: %s" % len(self.triggered_bug_information))
            # self.logger.info("----------------------------------------")
            # self.logger.info(
            #     "the time needed to satisfy the precondition: %s" % self.time_needed_to_satisfy_precondition)
            # self.logger.info("How many times check the property: %s" % len(self.time_to_check_rule))
            # self.logger.info("the time needed to check the property: %s" % self.time_to_check_rule)
        else:
            self.logger.info("did not satisfy the precondition")

        if len(self.triggered_bug_information) > 0:
            self.logger.info("the action count, time needed to trigger the bug, and the property name: %s" % self.triggered_bug_information)
        else:
            self.logger.info("did not trigger the bug")

        # for rule in self.rules:
        #     self.logger.info("property: %s, #satisfy precondition: %d, #check property: %d, #trigger the bug: %d" % (
        #         rule, self.rules[rule][RULE_STATE.SATISFY_PRE], self.rules[rule][RULE_STATE.CHECK_PROPERTY],
        #         self.rules[rule][RULE_STATE.TRIGGER_BUG]))


class GuidedPolicy(KeaInputPolicy):
    """
    
    """

    def __init__(self, device, app, random_input, kea_core=None):
        super(GuidedPolicy, self).__init__(
            device, app, random_input, kea_core
        )
        self.logger = logging.getLogger(self.__class__.__name__)
        self.list_main_path = self.kea_core.get_mainPath_list()
        if self.list_main_path:
            self.logger.info("main path with length %d" % len(self.list_main_path))
        else:
            self.logger.error("no main path is found")

        self.__num_restarts = 0
        self.__num_steps_outside = 0
        self.__event_trace = ""
        self.__missed_states = set()

        self.execute_main_path = True

        self.current_index_on_main_path = 0
        self.max_number_of_mutate_steps_on_single_node = 20
        self.current_number_of_mutate_steps_on_single_node = 0
        self.number_of_events_that_try_to_find_event_on_main_path = 0
        self.index_on_main_path_after_mutation = -1

        self.last_random_text = None
        self.last_rotate_events = KEY_RotateDeviceNeutralEvent

    def select_main_path(self):
        if len(self.list_main_path) == 0:
            self.logger.error("main path is empty")
            return
        self.main_path = random.choice(self.list_main_path)
        self.path_func, self.main_path =  self.kea_core.get_mainPath(self.main_path)
        self.logger.info("select the main path function: %s" % self.path_func)
        self.main_path_list = copy.deepcopy(self.main_path)
        self.max_number_of_events_that_try_to_find_event_on_main_path = min(10, len(self.main_path))
        self.mutate_node_index_on_main_path = len(self.main_path)


    def generate_event(self):
        """
        
        """

        self.current_state = self.device.get_current_state(self.action_count)

        #Return relevant events based on whether the application is in the foreground.
        event = self.check_the_app_on_foreground()
        if event is not None:
            self.update_utg()
            self.last_state = self.current_state
            self.last_event = event
            return event
        if (self.action_count == ACTION_COUNT_TO_START and self.current_index_on_main_path == 0) or isinstance(self.last_event, ReInstallAppEvent):
            self.select_main_path()
            if isinstance(self.last_event, ReInstallAppEvent):
                self.update_utg()
                self.last_state = self.current_state
                self.last_event = event
                initialize_start_event = U2StartEvent("InitializeStart")
                self.update_node(initialize_start_event, self.last_state)
                self.run_initial_rules()
                return None
            self.run_initial_rules()
            time.sleep(2)
        if self.execute_main_path:
            event_str = self.get_main_path_event()
            if event_str:
                if 0 < self.current_index_on_main_path < self.mutate_node_index_on_main_path:
                    self.action_count -= 1
                self.logger.info("*****main path running*****")
                self.kea_core.exec_mainPath(event_str)
                self.last_state = self.current_state
                self.last_event = event
                return None
        else:
            self.update_utg()
        if event is None:
            event = self.mutate_the_main_path()

        self.last_state = self.current_state
        self.last_event = event
        return event

    def end_mutation(self):
        self.index_on_main_path_after_mutation = -1
        self.number_of_events_that_try_to_find_event_on_main_path = 0
        self.execute_main_path = True
        self.current_number_of_mutate_steps_on_single_node = 0
        self.current_index_on_main_path = 0
        self.mutate_node_index_on_main_path -= 1
        if self.mutate_node_index_on_main_path == -1:
            self.mutate_node_index_on_main_path = len(self.main_path)
            return ReInstallAppEvent(app=self.app)
        self.logger.info("reach the max number of mutate steps on single node, restart the app")
        return KillAndRestartAppEvent(app=self.app)

    def check_property_with_probability(self, p=0.5):
        """
        try to check property with probability (default 50%)
        return 1 if the property has been checked.
        """
        rules_to_check = self.kea_core.get_rules_that_pass_the_preconditions()

        if len(rules_to_check) > 0:
            t = self.time_recoder.get_time_duration()
            self.time_needed_to_satisfy_precondition.append(t)
            self.logger.info(
                "has rule that matches the precondition and the time duration is " + self.time_recoder.get_time_duration())
            if random.random() < p:
                self.time_to_check_rule.append(t)
                self.logger.info(" check rule")
                # self.update_utg()
                check_start_event = U2StartEvent("CheckStart")
                self.update_node(check_start_event, self.last_state)
                self.check_rule_with_precondition()
                return 1
            else:
                self.logger.info("don't check rule")

    def mutate_the_main_path(self):
        event = None
        self.current_number_of_mutate_steps_on_single_node += 1

        if self.current_number_of_mutate_steps_on_single_node >= self.max_number_of_mutate_steps_on_single_node:

            if self.number_of_events_that_try_to_find_event_on_main_path <= self.max_number_of_events_that_try_to_find_event_on_main_path:
                self.number_of_events_that_try_to_find_event_on_main_path += 1
                if self.index_on_main_path_after_mutation == len(self.main_path_list):
                    self.logger.info("reach the end of the main path")
                    rules_to_check = self.kea_core.get_rules_that_pass_the_preconditions()
                    if len(rules_to_check) > 0:
                        t = self.time_recoder.get_time_duration()
                        self.time_needed_to_satisfy_precondition.append(t)
                        self.check_rule_with_precondition()
                    return self.end_mutation()


                event_str = self.get_event_from_main_path()
                try:
                    self.kea_core.exec_mainPath(event_str)
                    self.logger.info("find the event in the main path")
                    return None
                except Exception:
                    self.logger.info("can't find the event in the main path")
                    return self.end_mutation()

            return self.end_mutation()

        self.index_on_main_path_after_mutation = -1

        if self.check_property_with_probability() == 1:
            # if the property has been checked, don't return any event
            return None

        event = self.generate_explore_event()
        return event

    def get_main_path_event(self):
        """
        
        """
        if self.current_index_on_main_path == self.mutate_node_index_on_main_path:
            self.logger.info(
                "reach the mutate index, start mutate on the node %d" % self.mutate_node_index_on_main_path)
            self.execute_main_path = False
            return None
        if self.current_index_on_main_path == 0:
            self.current_state = self.device.get_current_state(self.action_count)
            self.update_utg()
            self.last_state = self.current_state
            mainPath_start_event = U2StartEvent("MainPathStart")
            self.update_node(mainPath_start_event, self.last_state)

        self.logger.info("execute node index on main path: %d" % self.current_index_on_main_path)
        u2_event_str = self.main_path_list[self.current_index_on_main_path]
        if u2_event_str is None:
            self.logger.warning("event is None on main path node %d" % self.current_index_on_main_path)
            self.current_index_on_main_path += 1
            return self.get_main_path_event()
        self.current_index_on_main_path += 1
        return u2_event_str

    def get_event_from_main_path(self):
        """
        
        """
        if self.index_on_main_path_after_mutation == -1:
            for i in range(len(self.main_path_list) - 1, -1, -1):

                event_str = self.main_path_list[i]
                if event_str is None:
                    continue
                self.index_on_main_path_after_mutation = i + 1
                return event_str
        else:
            event_str = self.main_path_list[self.index_on_main_path_after_mutation]
            if event_str is None:
                return None

            self.index_on_main_path_after_mutation += 1
            return event_str
        return None


    def generate_explore_event(self):
        """
        generate an event based on current UTG to explore the app
        @return: InputEvent
        """
        current_state = self.current_state
        self.logger.info("Current state: %s" % current_state.state_str)
        if current_state.state_str in self.__missed_states:
            self.__missed_states.remove(current_state.state_str)

        if current_state.get_app_activity_depth(self.app) < 0:
            # If the app is not in the activity stack
            start_app_intent = self.app.get_start_intent()

            # It seems the app stucks at some state, has been
            # 1) force stopped (START, STOP)
            #    just start the app again by increasing self.__num_restarts
            # 2) started at least once and cannot be started (START)
            #    pass to let viewclient deal with this case
            # 3) nothing
            #    a normal start. clear self.__num_restarts.

            if self.__event_trace.endswith(
                    EVENT_FLAG_START_APP + EVENT_FLAG_STOP_APP
            ) or self.__event_trace.endswith(EVENT_FLAG_START_APP):
                self.__num_restarts += 1
                self.logger.info(
                    "The app had been restarted %d times.", self.__num_restarts
                )
            else:
                self.__num_restarts = 0

            # pass (START) through
            if not self.__event_trace.endswith(EVENT_FLAG_START_APP):
                if self.__num_restarts > MAX_NUM_RESTARTS:
                    # If the app had been restarted too many times, enter random mode
                    msg = "The app had been restarted too many times. Entering random mode."
                    self.logger.info(msg)
                    self.__random_explore = True
                else:
                    # Start the app
                    self.__event_trace += EVENT_FLAG_START_APP
                    self.logger.info("Trying to start the app...")
                    return IntentEvent(intent=start_app_intent)

        elif current_state.get_app_activity_depth(self.app) > 0:
            # If the app is in activity stack but is not in foreground
            self.__num_steps_outside += 1

            if self.__num_steps_outside > MAX_NUM_STEPS_OUTSIDE:
                # If the app has not been in foreground for too long, try to go back
                if self.__num_steps_outside > MAX_NUM_STEPS_OUTSIDE_KILL:
                    stop_app_intent = self.app.get_stop_intent()
                    go_back_event = IntentEvent(stop_app_intent)
                else:
                    go_back_event = KeyEvent(name="BACK")
                self.__event_trace += EVENT_FLAG_NAVIGATE
                self.logger.info("Going back to the app...")
                return go_back_event
        else:
            # If the app is in foreground
            self.__num_steps_outside = 0

        # Get all possible input events
        possible_events = current_state.get_possible_input()

        if self.random_input:
            random.shuffle(possible_events)
        possible_events.append(KeyEvent(name="BACK"))
        possible_events.append(RotateDevice())

        self.__event_trace += EVENT_FLAG_EXPLORE

        event = random.choice(possible_events)
        if isinstance(event, RotateDevice):
            if self.last_rotate_events == KEY_RotateDeviceNeutralEvent:
                self.last_rotate_events = KEY_RotateDeviceRightEvent
                event = RotateDeviceRightEvent()
            else:
                self.last_rotate_events = KEY_RotateDeviceNeutralEvent
                event = RotateDeviceNeutralEvent()

        return event

    def check_the_app_on_foreground(self):
        if self.current_state.get_app_activity_depth(self.app) < 0:
            # If the app is not in the activity stack
            start_app_intent = self.app.get_start_intent()

            # It seems the app stucks at some state, has been
            # 1) force stopped (START, STOP)
            #    just start the app again by increasing self.__num_restarts
            # 2) started at least once and cannot be started (START)
            #    pass to let viewclient deal with this case
            # 3) nothing
            #    a normal start. clear self.__num_restarts.

            if self.__event_trace.endswith(
                    EVENT_FLAG_START_APP + EVENT_FLAG_STOP_APP
            ) or self.__event_trace.endswith(EVENT_FLAG_START_APP):
                self.__num_restarts += 1
                self.logger.info(
                    "The app had been restarted %d times.", self.__num_restarts
                )
            else:
                self.__num_restarts = 0

            # pass (START) through
            if not self.__event_trace.endswith(EVENT_FLAG_START_APP):
                if self.__num_restarts > MAX_NUM_RESTARTS:
                    # If the app had been restarted too many times, enter random mode
                    msg = "The app had been restarted too many times. Entering random mode."
                    self.logger.info(msg)
                    self.__random_explore = True
                else:
                    # Start the app
                    self.__event_trace += EVENT_FLAG_START_APP
                    self.logger.info("Trying to start the app...")
                    return IntentEvent(intent=start_app_intent)

        elif self.current_state.get_app_activity_depth(self.app) > 0:
            # If the app is in activity stack but is not in foreground
            self.__num_steps_outside += 1

            if self.__num_steps_outside > MAX_NUM_STEPS_OUTSIDE:
                # If the app has not been in foreground for too long, try to go back
                if self.__num_steps_outside > MAX_NUM_STEPS_OUTSIDE_KILL:
                    stop_app_intent = self.app.get_stop_intent()
                    go_back_event = IntentEvent(stop_app_intent)
                else:
                    go_back_event = KeyEvent(name="BACK")
                self.__event_trace += EVENT_FLAG_NAVIGATE
                self.logger.info("Going back to the app...")
                return go_back_event
        else:
            # If the app is in foreground
            self.__num_steps_outside = 0

class RandomPolicy(KeaInputPolicy):
    """
    random input policy based on UTG
    """

    def __init__(self, device, app, random_input=True, kea_core=None, restart_app_after_check_property=False,
                 number_of_events_that_restart_app=100, clear_and_restart_app_data_after_100_events=False):
        super(RandomPolicy, self).__init__(
            device, app, random_input, kea_core
        )
        self.restart_app_after_check_property = restart_app_after_check_property
        self.number_of_events_that_restart_app = number_of_events_that_restart_app
        self.clear_and_restart_app_data_after_100_events = clear_and_restart_app_data_after_100_events
        self.logger = logging.getLogger(self.__class__.__name__)

        self.preferred_buttons = [
            "yes",
            "ok",
            "activate",
            "detail",
            "more",
            "access",
            "allow",
            "check",
            "agree",
            "try",
            "go",
            "next",
        ]
        self.__num_restarts = 0
        self.__num_steps_outside = 0
        self.__event_trace = ""
        self.__missed_states = set()
        self.number_of_steps_outside_the_shortest_path = 0
        self.reached_state_on_the_shortest_path = []

        self.last_rotate_events = KEY_RotateDeviceNeutralEvent

    def generate_event(self):
        """
        generate an event
        @return:
        """

        if self.action_count == ACTION_COUNT_TO_START or isinstance(self.last_event, ReInstallAppEvent): 
            if isinstance(self.last_event, ReInstallAppEvent):
                self.current_state = self.device.get_current_state(self.action_count)
                self.update_utg()
                self.last_state = self.current_state
                initialize_start_event = U2StartEvent("InitializeStart")
                self.update_node(initialize_start_event, self.last_state)
                self.run_initial_rules()
                return None
            self.run_initial_rules()
        # Get current device state
        self.current_state = self.device.get_current_state(self.action_count)
        if self.current_state is None:
            import time
            time.sleep(5)
            return KeyEvent(name="BACK")

        self.update_utg()

        if self.action_count % self.number_of_events_that_restart_app == 0 and self.clear_and_restart_app_data_after_100_events:
            self.logger.info("clear and restart app after %s events" % self.number_of_events_that_restart_app)
            return ReInstallAppEvent(self.app)
        rules_to_check = self.kea_core.get_rules_that_pass_the_preconditions()

        if len(rules_to_check) > 0:
            t = self.time_recoder.get_time_duration()
            self.time_needed_to_satisfy_precondition.append(t)
            self.logger.debug(
                "has rule that matches the precondition and the time duration is " + self.time_recoder.get_time_duration())
            if random.random() < 0.5:
                self.time_to_check_rule.append(t)
                self.logger.info(" check rule")
                check_start_event = U2StartEvent("CheckStart")
                self.update_node(check_start_event, self.last_state)
                self.check_rule_with_precondition()
                if self.restart_app_after_check_property:
                    self.logger.debug("restart app after check property")
                    return KillAppEvent(app=self.app)
                return None
            else:
                self.logger.info("don't check rule")
        event = None

        if event is None:
            event = self.generate_event_based_on_utg()

        if isinstance(event, RotateDevice):
            if self.last_rotate_events == KEY_RotateDeviceNeutralEvent:
                self.last_rotate_events = KEY_RotateDeviceRightEvent
                event = RotateDeviceRightEvent()
            else:
                self.last_rotate_events = KEY_RotateDeviceNeutralEvent
                event = RotateDeviceNeutralEvent()

        self.last_state = self.current_state
        self.last_event = event
        return event

    def generate_event_based_on_utg(self):
        """
        generate an event based on current UTG
        @return: InputEvent
        """
        current_state = self.current_state
        self.logger.debug("Current state: %s" % current_state.state_str)
        if current_state.state_str in self.__missed_states:
            self.__missed_states.remove(current_state.state_str)

        #Get the depth of the app's activity in the activity stack
        if current_state.get_app_activity_depth(self.app) < 0:
            # If the app is not in the activity stack
            start_app_intent = self.app.get_start_intent()

            # It seems the app stucks at some state, has been
            # 1) force stopped (START, STOP)
            #    just start the app again by increasing self.__num_restarts
            # 2) started at least once and cannot be started (START)
            #    pass to let viewclient deal with this case
            # 3) nothing
            #    a normal start. clear self.__num_restarts.

            if self.__event_trace.endswith(
                    EVENT_FLAG_START_APP + EVENT_FLAG_STOP_APP
            ) or self.__event_trace.endswith(EVENT_FLAG_START_APP):
                self.__num_restarts += 1
                self.logger.debug(
                    "The app had been restarted %d times.", self.__num_restarts
                )
            else:
                self.__num_restarts = 0

            # pass (START) through
            if not self.__event_trace.endswith(EVENT_FLAG_START_APP):
                if self.__num_restarts > MAX_NUM_RESTARTS:
                    # If the app had been restarted too many times, enter random mode
                    msg = "The app had been restarted too many times. Entering random mode."
                    self.logger.debug(msg)
                    self.__random_explore = True
                else:
                    # Start the app
                    self.__event_trace += EVENT_FLAG_START_APP
                    self.logger.debug("Trying to start the app...")
                    return IntentEvent(intent=start_app_intent)

        elif current_state.get_app_activity_depth(self.app) > 0:
            # If the app is in activity stack but is not in foreground
            self.__num_steps_outside += 1

            if self.__num_steps_outside > MAX_NUM_STEPS_OUTSIDE:
                # If the app has not been in foreground for too long, try to go back
                if self.__num_steps_outside > MAX_NUM_STEPS_OUTSIDE_KILL:
                    stop_app_intent = self.app.get_stop_intent()
                    go_back_event = IntentEvent(stop_app_intent)
                else:
                    go_back_event = KeyEvent(name="BACK")
                self.__event_trace += EVENT_FLAG_NAVIGATE
                self.logger.debug("Going back to the app...")
                return go_back_event
        else:
            # If the app is in foreground
            self.__num_steps_outside = 0

        possible_events = current_state.get_possible_input()

        if self.random_input:
            random.shuffle(possible_events)
        possible_events.append(KeyEvent(name="BACK"))
        possible_events.append(RotateDevice())

        self.__event_trace += EVENT_FLAG_EXPLORE
        return random.choice(possible_events)

