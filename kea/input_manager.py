import json
import logging
import time

from .similarity import Similarity

from .input_event import EventLog
from .input_policy import (
    GuidedPolicy,
    POLICY_GUIDED,
    POLICY_RANDOM,
    KeaInputPolicy,
    RandomPolicy,
    POLICY_NONE,
    POLICY_LLM,
    LLMPolicy
)

DEFAULT_POLICY = POLICY_RANDOM
RANDOM_POLICY = POLICY_RANDOM
DEFAULT_EVENT_INTERVAL = 1
DEFAULT_EVENT_COUNT = 100000000
DEFAULT_TIMEOUT = 3600
DEFAULT_DEVICE_SERIAL = "emulator-5554"
DEFAULT_UI_TARPIT_NUM = 2

class UnknownInputException(Exception):
    pass


class InputManager(object):
    """
    This class manages all events to send during app running
    """

    def __init__(
        self,
        device,
        app,
        policy_name,
        random_input,
        event_interval,
        event_count=DEFAULT_EVENT_COUNT,  # the number of event generated in the explore phase.
        script_path=None,
        profiling_method=None,
        master=None,
        replay_output=None,
        kea=None,
        number_of_events_that_restart_app=100,
        generate_utg=False
    ):
        """
        manage input event sent to the target device
        :param device: instance of Device
        :param app: instance of App
        :param policy_name: policy of generating events, string
        :return:
        """
        self.logger = logging.getLogger('InputEventManager')
        self.enabled = True

        self.device = device
        self.app = app
        self.policy_name = policy_name
        self.random_input = random_input
        self.events = []
        self.policy = None
        self.script = None
        self.event_count = event_count
        self.event_interval = event_interval
        self.replay_output = replay_output

        self.monkey = None

        if script_path is not None:
            f = open(script_path, 'r')
            script_dict = json.load(f)
            from .input_script import DroidBotScript

            self.script = DroidBotScript(script_dict)

        self.kea = kea
        
        self.profiling_method = profiling_method
        self.number_of_events_that_restart_app = number_of_events_that_restart_app
        self.generate_utg = generate_utg
        self.policy = self.get_input_policy(device, app, master)
        self.sim_calculator = Similarity(DEFAULT_UI_TARPIT_NUM)

    def get_input_policy(self, device, app, master):
        if self.policy_name == POLICY_NONE:
            input_policy = None
        elif self.policy_name == POLICY_GUIDED:
            input_policy = GuidedPolicy(
                device,
                app,
                self.kea,
                self.generate_utg
            )
        elif self.policy_name == POLICY_RANDOM:
            input_policy = RandomPolicy(device, app, kea=self.kea, number_of_events_that_restart_app = self.number_of_events_that_restart_app, clear_and_reinstall_app=True, generate_utg = self.generate_utg)
        elif self.policy_name == POLICY_LLM:
            input_policy = LLMPolicy(device, app, kea=self.kea, number_of_events_that_restart_app = self.number_of_events_that_restart_app, clear_and_restart_app_data_after_100_events=True, generate_utg = self.generate_utg)
        else:
            self.logger.warning(
                "No valid input policy specified. Using policy \"none\"."
            )
            input_policy = None
        if isinstance(input_policy, KeaInputPolicy):
            input_policy.script = self.script
            input_policy.master = master
        return input_policy

    def add_event(self, event):
        """
        add one event to the event list
        :param event: the event to be added, should be subclass of AppEvent
        :return:
        """
        if event is None:
            return
        self.events.append(event)

        #Record and send events to the device.
        event_log = EventLog(self.device, self.app, event, self.profiling_method)
        event_log.start()
        while True:
            time.sleep(self.event_interval)
            if not self.device.pause_sending_event:
                break

        event_log.stop()

    def start(self):
        """
        start sending event
        """
        self.logger.info("start sending events, policy is %s" % self.policy_name)

        try:
            if self.policy is not None:
                self.policy.start(self)

        except KeyboardInterrupt:
            pass

        self.stop()
        self.logger.info("Finish sending events")

    def stop(self):
        """
        stop sending event
        """
        if self.monkey:
            if self.monkey.returncode is None:
                self.monkey.terminate()
            self.monkey = None
            pid = self.device.get_app_pid("com.android.commands.monkey")
            if pid is not None:
                self.device.adb.shell("kill -9 %d" % pid)
        self.enabled = False
