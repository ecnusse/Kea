from asyncio import sleep
from dataclasses import dataclass
import os

import logging
import random
import copy
import re
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
    SetTextEvent
)
from .utg import UTG
from kea import utils
from kea.kea import CHECK_RESULT
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .input_manager import InputManager
    from .core import Kea
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
# Max number of query llm
MAX_NUM_QUERY_LLM = 10

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
POLICY_LLM = "llm"

@dataclass
class RULE_STATE:
    SATISFY_PRE = "#satisfy pre"
    CHECK_PROPERTY = "#check property"
    TRIGGER_BUG = "#trigger the bug"

class InputInterruptedException(Exception):
    pass

class InputPolicy(object):
    """
    This class is responsible for generating events to stimulate more app behaviour
    It should call AppEventManager.send_event method continuously
    """

    def __init__(self, device:"Device", app:"App", kea:"Kea"=None):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.time_recoder = Time()

        self.device = device
        self.app = app
        self.action_count = 0
        self.master = None
        self.kea = kea
        self.input_manager = None
        self.time_needed_to_satisfy_precondition = []

        self.time_to_check_rule = []

        self.last_event = None
        self.from_state = None
        self.to_state = None
        self.generate_utg = False
        self.triggered_bug_information = []

    def run_initial_rules(self):
        if len(self.kea.initializer) == 0:
            self.logger.warning("No initializer")
            return
        

        result = self.kea.execute_rules(self.kea.initializer)
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
                if hasattr(self.device, "u2"):
                    self.device.u2.set_fastinput_ime(True)

                self.logger.info("Exploration action count: %d" % self.action_count)

                if self.action_count == 0 and self.master is None:
                    #If the application is running, close the application.
                    event = KillAppEvent(app=self.app)
                elif self.action_count == 1 and self.master is None:
                    event = IntentEvent(self.app.get_start_intent())
                else:
                    event = self.generate_event()
                if event is not None:
                    self.from_state = self.device.save_screenshot_for_report(event=event)
                    input_manager.add_event(event)
                    self.to_state = self.device.get_current_state()
                    self.last_event = event
                    if self.generate_utg:
                        self.update_utg()

                bug_report_path = os.path.join(self.device.output_dir, "all_states")
                utils.generate_report(bug_report_path, self.device.output_dir, self.triggered_bug_information, self.time_needed_to_satisfy_precondition, self.device.get_count(), self.time_recoder.get_time_duration())
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

    def update_utg(self):
        self.utg.add_transition(self.last_event, self.from_state, self.to_state)

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

    def __init__(self, device, app, random_input, kea=None):
        super(KeaInputPolicy, self).__init__(device, app, kea)
        self.random_input = random_input
        self.script = None
        self.master = None
        self.script_events = []
        self.last_event = None
        self.from_state = None
        self.to_state = None
        self.utg = UTG(
            device=device, app=app, random_input=random_input
        )
        self.script_event_idx = 0
        if self.device.humanoid is not None:
            self.humanoid_view_trees = []
            self.humanoid_events = []
        
        # retrive all the rules from the provided properties
        self.rules = {}
        for rule in self.kea.all_rules:
            self.rules[rule.function.__name__] = {RULE_STATE.SATISFY_PRE: 0, RULE_STATE.CHECK_PROPERTY: 0, RULE_STATE.TRIGGER_BUG: 0}
        # record the action count, time and property name when the bug is triggered
        self.triggered_bug_information = []

    def check_rule_with_precondition(self):
        rules_list_to_check = self.kea.get_rules_that_pass_the_preconditions()
        if len(rules_list_to_check) == 0:
            self.logger.debug("No rules match the precondition")
            if hasattr(self, "not_reach_precondition_path_number"):
                self.not_reach_precondition_path_number.append(self.path_index)
            return
            # continue

        for rule in rules_list_to_check:
            self.rules[rule.function.__name__][RULE_STATE.SATISFY_PRE] += 1
        rule_to_check = random.choice(rules_list_to_check)

        if rule_to_check is not None:
            self.logger.info(f"-------Check Property : {rule_to_check}------")
            self.rules[rule_to_check.function.__name__][RULE_STATE.CHECK_PROPERTY] += 1
            pre_id = self.device.get_count()
            # check rule, record relavant info and output log
            result = self.kea.execute_rule(rule_to_check)
            if result == CHECK_RESULT.ASSERTION_ERROR:
                self.logger.error(f"-------Postcondition failed. Assertion error, Property:{rule_to_check}------")
                self.logger.debug("-------time from start : %s-----------" % str(self.time_recoder.get_time_duration()))
                self.rules[rule_to_check.function.__name__][RULE_STATE.TRIGGER_BUG] += 1
                post_id = self.device.get_count()
                self.triggered_bug_information.append(
                    ((pre_id, post_id), self.time_recoder.get_time_duration(), rule_to_check.function.__name__))


            elif result == CHECK_RESULT.PASS:
                self.logger.info(f"-------Post condition satisfied. Property:{rule_to_check} pass------")
                self.logger.debug("-------time from start : %s-----------" % str(self.time_recoder.get_time_duration()))

            elif result == CHECK_RESULT.UI_NOT_FOUND:
                self.logger.error(f"-------Execution failed: UiObjectNotFound during exectution. Property:{rule_to_check}-----------")

            elif result == CHECK_RESULT.PRECON_NOT_SATISFIED:
                self.logger.info("-------Precondition not satisfied-----------")
            
            else:
                raise AttributeError(f"Invalid property checking result {result}")

    def check_rule_without_precondition(self):
        rules_to_check = self.kea.get_rules_without_preconditions()
        if len(rules_to_check) > 0:
            result = self.kea.execute_rules(
                self.kea.get_rules_without_preconditions()
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
        self.utg.add_transition(self.last_event, self.from_state, self.to_state)


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
        bug_report_path = os.path.join(self.device.output_dir, "all_states")
        utils.generate_report(bug_report_path, self.device.output_dir, self.triggered_bug_information, self.time_needed_to_satisfy_precondition, self.device.get_count(), self.time_recoder.get_time_duration())
        # self.logger.info("----------------------------------------")
        #
        # if len(self.triggered_bug_information) > 0:
        #     self.logger.info("Time needed to trigger the first bug: %s" % self.triggered_bug_information[0][1])
        #
        # if len(self.time_needed_to_satisfy_precondition) > 0:
        #     self.logger.info(
        #         "Time needed to satisfy the first precondition: %s" % self.time_needed_to_satisfy_precondition[0])
        #     self.logger.info(
        #         "The precondition(s) is/are satisfied %s times" % len(self.time_needed_to_satisfy_precondition))
        #     if len(self.triggered_bug_information) > 0:
        #         self.logger.info("Triggered %s bug:" % len(self.triggered_bug_information))
        # else:
        #     self.logger.info("No precondition has been satisfied.")
        #
        # if len(self.triggered_bug_information) > 0:
        #     self.logger.info("the action count, time needed to trigger the bug, and the property name: %s" % self.triggered_bug_information)
        # else:
        #     self.logger.info("No bug has been triggered.")


class GuidedPolicy(KeaInputPolicy):
    """
    
    """

    def __init__(self, device, app, random_input, kea=None, generate_utg = False):
        super(GuidedPolicy, self).__init__(
            device, app, random_input, kea
        )
        self.logger = logging.getLogger(self.__class__.__name__)
        
        if len(self.kea.all_mainPaths):
            self.logger.info("Found %d mainPaths" % len(self.kea.all_mainPaths))
        else:
            self.logger.error("No mainPath found")

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

        self.generate_utg = generate_utg

    def select_main_path(self):
        if len(self.kea.all_mainPaths) == 0:
            self.logger.error("No mainPath")
            return
        self.main_path = random.choice(self.kea.all_mainPaths)
        self.path_func, self.main_path =  self.kea.parse_mainPath(self.main_path)
        self.logger.info(f"Select the {len(self.main_path)} steps mainPath function: {self.path_func}")
        self.main_path_list = copy.deepcopy(self.main_path)
        self.max_number_of_events_that_try_to_find_event_on_main_path = min(10, len(self.main_path))
        self.mutate_node_index_on_main_path = len(self.main_path)


    def generate_event(self):
        """
        
        """

        current_state = self.device.get_current_state()

        #Return relevant events based on whether the application is in the foreground.

        event = self.check_the_app_on_foreground(current_state)
        if event is not None:
            return event


        if (self.action_count == ACTION_COUNT_TO_START and self.current_index_on_main_path == 0) or isinstance(self.last_event, ReInstallAppEvent):
            self.select_main_path()
            self.run_initial_rules()
            time.sleep(2)
        if self.execute_main_path:
            event_str = self.get_main_path_event()
            if event_str:
                self.logger.info("*****main path running*****")
                self.kea.exec_mainPath(event_str)
                return None
        if event is None:
            event = self.mutate_the_main_path()

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
        rules_list_to_check = self.kea.get_rules_that_pass_the_preconditions()

        if len(rules_list_to_check) > 0:
            t = self.time_recoder.get_time_duration()
            self.time_needed_to_satisfy_precondition.append(t)
            self.logger.info(f"Found {len(rules_list_to_check)} rules satisfied the precondition. Current execution time {self.time_recoder.get_time_duration()}")
            if random.random() < p:
                self.time_to_check_rule.append(t)
                self.logger.info(" check rule")
                self.check_rule_with_precondition()
                return 1
            else:
                self.logger.info("Found exectuable property in current state. No property will be checked now according to the random checking policy.")

    def mutate_the_main_path(self):
        event = None
        self.current_number_of_mutate_steps_on_single_node += 1

        if self.current_number_of_mutate_steps_on_single_node >= self.max_number_of_mutate_steps_on_single_node:

            if self.number_of_events_that_try_to_find_event_on_main_path <= self.max_number_of_events_that_try_to_find_event_on_main_path:
                self.number_of_events_that_try_to_find_event_on_main_path += 1
                if self.index_on_main_path_after_mutation == len(self.main_path_list):
                    self.logger.info("reach the end of the main path")
                    rules_to_check = self.kea.get_rules_that_pass_the_preconditions()
                    if len(rules_to_check) > 0:
                        t = self.time_recoder.get_time_duration()
                        self.time_needed_to_satisfy_precondition.append(t)
                        self.check_rule_with_precondition()
                    return self.end_mutation()


                event_str = self.get_event_from_main_path()
                try:
                    self.kea.exec_mainPath(event_str)
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
        current_state = self.device.get_current_state()
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

    def check_the_app_on_foreground(self, current_state):
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

class RandomPolicy(KeaInputPolicy):
    """
    random input policy based on UTG
    """

    def __init__(self, device, app, random_input=True, kea=None, restart_app_after_check_property=False,
                 number_of_events_that_restart_app=100, clear_and_restart_app_data_after_100_events=False, generate_utg=False):
        super(RandomPolicy, self).__init__(
            device, app, random_input, kea
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

        self.generate_utg = generate_utg

    def generate_event(self):
        """
        generate an event
        @return:
        """

        if self.action_count == ACTION_COUNT_TO_START or isinstance(self.last_event, ReInstallAppEvent):
            self.run_initial_rules()
        current_state = self.device.get_current_state()
        if current_state is None:
            import time
            time.sleep(5)
            return KeyEvent(name="BACK")


        if self.action_count % self.number_of_events_that_restart_app == 0 and self.clear_and_restart_app_data_after_100_events:
            self.logger.info("clear and restart app after %s events" % self.number_of_events_that_restart_app)
            return ReInstallAppEvent(self.app)
        rules_to_check = self.kea.get_rules_that_pass_the_preconditions()

        if len(rules_to_check) > 0:
            t = self.time_recoder.get_time_duration()
            self.time_needed_to_satisfy_precondition.append(t)
            self.logger.debug("has rule that matches the precondition and the time duration is " + self.time_recoder.get_time_duration())
            if random.random() < 0.5:
                self.time_to_check_rule.append(t)
                self.logger.info("Check property")
                self.check_rule_with_precondition()
                if self.restart_app_after_check_property:
                    self.logger.debug("restart app after check property")
                    return KillAppEvent(app=self.app)
                return None
            else:
                self.logger.info("Found exectuable property in current state. No property will be checked now according to the random checking policy.")
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

        return event

    def generate_event_based_on_utg(self):
        """
        generate an event based on current UTG
        @return: InputEvent
        """
        current_state = self.device.get_current_state()
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
    
class LLMPolicy(RandomPolicy):
    '''
    use LLM to generate input when detected ui tarpit
    '''
    def __init__(self, device, app, random_input=True, kea=None, restart_app_after_check_property=False,
                 number_of_events_that_restart_app=100, clear_and_restart_app_data_after_100_events=False, generate_utg=False):
        super(LLMPolicy, self).__init__(
            device, app, random_input, kea
        )
        self.logger = logging.getLogger(self.__class__.__name__)
        self.__action_history=[]
        self.__all_action_history=set()
        self.__activity_history = set()
        self.from_state = None
        self.__missed_states = set()
        self.task = "You are an expert in App GUI testing. Please guide the testing tool to enhance the coverage of functional scenarios in testing the App based on your extensive App testing experience. "

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
                if hasattr(self.device, "u2"):
                    self.device.u2.set_fastinput_ime(True)

                self.logger.info("Exploration action count: %d" % self.action_count)

                if self.action_count == 0 and self.master is None:
                    #If the application is running, close the application.
                    event = KillAppEvent(app=self.app)
                elif self.action_count == 1 and self.master is None:
                    event = IntentEvent(self.app.get_start_intent())
                else:
                    if input_manager.sim_calculator.detected_ui_tarpit(input_manager):
                        # If detected a ui tarpit
                        if input_manager.sim_calculator.sim_count > MAX_NUM_QUERY_LLM:
                            # If query LLM too much
                            self.logger.info(f'query too much. go back!')
                            event = KeyEvent(name="BACK")
                            self.clear_action_history()
                            input_manager.sim_calculator.sim_count = 0 
                        else:
                            # stop random policy, start query LLM
                            event = self.generate_llm_event()
                    else:
                        event = self.generate_event()

                if event is not None:
                    self.from_state = self.device.save_screenshot_for_report(event=event)
                    input_manager.add_event(event)
                    self.to_state = self.device.get_current_state()
                    self.last_event = event
                    if self.generate_utg:
                        self.update_utg()

                bug_report_path = os.path.join(self.device.output_dir, "all_states")
                utils.generate_report(bug_report_path, self.device.output_dir, self.triggered_bug_information, self.time_needed_to_satisfy_precondition, self.device.get_count(), self.time_recoder.get_time_duration())
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

    def generate_llm_event(self):
        """
        generate an LLM event
        @return:
        """

        if self.action_count == ACTION_COUNT_TO_START or isinstance(self.last_event, ReInstallAppEvent):
            self.run_initial_rules()
        current_state = self.device.get_current_state()
        if current_state is None:
            import time
            time.sleep(5)
            return KeyEvent(name="BACK")


        if self.action_count % self.number_of_events_that_restart_app == 0 and self.clear_and_restart_app_data_after_100_events:
            self.logger.info("clear and restart app after %s events" % self.number_of_events_that_restart_app)
            return ReInstallAppEvent(self.app)
        rules_to_check = self.kea.get_rules_that_pass_the_preconditions()

        if len(rules_to_check) > 0:
            t = self.time_recoder.get_time_duration()
            self.time_needed_to_satisfy_precondition.append(t)
            self.logger.debug("has rule that matches the precondition and the time duration is " + self.time_recoder.get_time_duration())
            if random.random() < 0.5:
                self.time_to_check_rule.append(t)
                self.logger.info("Check property")
                self.check_rule_with_precondition()
                if self.restart_app_after_check_property:
                    self.logger.debug("restart app after check property")
                    return KillAppEvent(app=self.app)
                return None
            else:
                self.logger.info("Found exectuable property in current state. No property will be checked now according to the random checking policy.")
        event = None

        if event is None:
            event = self.generate_llm_event_based_on_utg()

        if isinstance(event, RotateDevice):
            if self.last_rotate_events == KEY_RotateDeviceNeutralEvent:
                self.last_rotate_events = KEY_RotateDeviceRightEvent
                event = RotateDeviceRightEvent()
            else:
                self.last_rotate_events = KEY_RotateDeviceNeutralEvent
                event = RotateDeviceNeutralEvent()

        return event

    def generate_llm_event_based_on_utg(self):
        """
        generate an event based on current UTG
        @return: InputEvent
        """
        current_state = self.device.get_current_state()
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

            if self.__event_trace.endswith(EVENT_FLAG_START_APP + EVENT_FLAG_STOP_APP) \
                    or self.__event_trace.endswith(EVENT_FLAG_START_APP):
                self.__num_restarts += 1
                self.logger.info("The app had been restarted %d times.", self.__num_restarts)
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
                    self.__action_history = [f'- start the app {self.app.app_name}']
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
                self.__action_history.append('- go back')
                return go_back_event
        else:
            # If the app is in foreground
            self.__num_steps_outside = 0

        action, candidate_actions = self._get_action_with_LLM(current_state, self.__action_history,self.__activity_history,)
        if action is not None:
            self.__action_history.append(current_state.get_action_desc(action))
            self.__all_action_history.add(current_state.get_action_desc(action))
            return action

        if self.__random_explore:
            self.logger.info("Trying random event...")
            action = random.choice(candidate_actions)
            self.__action_history.append(current_state.get_action_desc(action))
            self.__all_action_history.add(current_state.get_action_desc(action))
            return action

        # If couldn't find a exploration target, stop the app
        stop_app_intent = self.app.get_stop_intent()
        self.logger.info("Cannot find an exploration target. Trying to restart app...")
        self.__action_history.append('- stop the app')
        self.__all_action_history.add('- stop the app')
        self.__event_trace += EVENT_FLAG_STOP_APP
        return IntentEvent(intent=stop_app_intent)
        
    def _query_llm(self, prompt, model_name='gpt-3.5-turbo'):
        # TODO: replace with your own LLM
        from openai import OpenAI
        gpt_url = '' 
        gpt_key = '' 
        client = OpenAI(
            base_url=gpt_url,
            api_key=gpt_key
        )

        messages=[{"role": "user", "content": prompt}]
        completion = client.chat.completions.create(
            messages=messages,
            model=model_name,
            timeout=30
        )
        res = completion.choices[0].message.content
        return res

    def _get_action_with_LLM(self, current_state, action_history,activity_history):
        activity = current_state.foreground_activity
        task_prompt = self.task +f"Currently, the App is stuck on the {activity} page, unable to explore more features. You task is to select an action based on the current GUI Infomation to perform next and help the app escape the UI tarpit."
        visisted_page_prompt = f'I have already visited the following activities: \n' + '\n'.join(activity_history)
        # all_history_prompt = f'I have already completed the following actions to explore the app: \n' + '\n'.join(all_action_history)
        history_prompt = f'I have already completed the following steps to leave {activity} page but failed: \n ' + ';\n '.join(action_history)
        state_prompt, candidate_actions = current_state.get_described_actions()
        question = 'Which action should I choose next? Just return the action id and nothing else.\nIf no more action is needed, return -1.'
        prompt = f'{task_prompt}\n{state_prompt}\n{visisted_page_prompt}\n{history_prompt}\n{question}'
        print(prompt)
        response = self._query_llm(prompt)
        print(f'response: {response}')

        match = re.search(r'\d+', response)
        if not match:
            return None, candidate_actions
        idx = int(match.group(0))
        selected_action = candidate_actions[idx]
        if isinstance(selected_action, SetTextEvent):
            view_text = current_state.get_view_desc(selected_action.view)
            question = f'What text should I enter to the {view_text}? Just return the text and nothing else.'
            prompt = f'{task_prompt}\n{state_prompt}\n{question}'
            print(prompt)
            response = self._query_llm(prompt)
            print(f'response: {response}')
            selected_action.text = response.replace('"', '')
            if len(selected_action.text) > 30:  # heuristically disable long text input
                selected_action.text = ''
        return selected_action, candidate_actions

    def get_last_state(self):
        return self.from_state

    def clear_action_history(self):
        self.__action_history = []