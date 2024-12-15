# This file contains the main class of droidbot
# It can be used after AVD was started, app was installed, and adb had been set up properly
# By configuring and creating a droidbot instance,
# droidbot will start interacting with Android in AVD like a human
import logging
import os
import sys
import pkg_resources
import shutil
from threading import Timer

from .env_manager import AppEnvManager
from .input_manager import InputManager

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .start import Setting

class DroidBot(object):
    """
    The main class of droidbot
    """

    # this is a single instance class
    instance = None

    def __init__(
        self,
        app_path=None,
        device_serial=None,
        is_emulator=False,
        output_dir=None,
        env_policy=None,
        policy_name=None,
        random_input=True,
        script_path=None,
        event_interval=None,
        event_count=0,
        timeout=None,
        keep_app=None,
        keep_env=False,
        cv_mode=False,
        debug_mode=False,
        profiling_method=None,
        grant_perm=False,
        send_document=True,
        enable_accessibility_hard=False,
        master=None,
        humanoid=None,
        ignore_ad=False,
        replay_output=None,
        kea=None,
        number_of_events_that_restart_app=100,
        run_initial_rules_after_every_mutation=True,
        is_harmonyos=False,
        is_package=False,
        generate_utg=False,
        settings:"Setting"=None
    ):
        """
        initiate droidbot with configurations
        :return:
        """
        if debug_mode:
            logging.basicConfig(level=logging.DEBUG,format='%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
        else:
            logging.basicConfig(level= logging.INFO)

        self.logger = logging.getLogger('DroidBot')
        DroidBot.instance = self
        self.output_dir = output_dir
        if output_dir is not None:
            #Clear the output left by the previous run to prevent JSON matching errors.
            if os.path.isdir(output_dir):
                shutil.rmtree(output_dir)
            os.makedirs(output_dir)
            html_index_path = pkg_resources.resource_filename(
                "kea", "resources/index.html"
            )
            stylesheets_path = pkg_resources.resource_filename(
                "kea", "resources/stylesheets"
            )
            target_stylesheets_dir = os.path.join(output_dir, "stylesheets")
            if os.path.exists(target_stylesheets_dir):
                shutil.rmtree(target_stylesheets_dir)
            shutil.copy(html_index_path, output_dir)
            shutil.copytree(stylesheets_path, target_stylesheets_dir)

        self.timeout = timeout
        self.timer = None
        self.keep_env = keep_env
        self.keep_app = keep_app

        self.device = None
        self.app = None
        self.droidbox = None
        self.env_manager = None
        self.input_manager = None
        self.enable_accessibility_hard = enable_accessibility_hard
        self.humanoid = humanoid
        self.ignore_ad = ignore_ad
        self.replay_output = replay_output

        self.enabled = True
        self.kea = kea

        # param initializer
        self.app_path = app_path
        self.device_serial = device_serial
        self.is_emulator = is_emulator
        self.env_policy = env_policy
        self.policy_name = policy_name
        self.random_input = random_input
        self.script_path = script_path
        self.event_interval = event_interval
        self.event_count = event_count
        self.cv_mode = cv_mode
        self.profiling_method = profiling_method
        self.grant_perm = grant_perm
        self.send_document = send_document
        self.master = master
        self.number_of_events_that_restart_app = number_of_events_that_restart_app
        self.run_initial_rules_after_every_mutation = run_initial_rules_after_every_mutation
        self.is_package = is_package
        self.generate_utg = generate_utg
        self.settings = settings
        try:
            self.init_droidbot(is_harmonyos)
        except Exception:
            import traceback

            traceback.print_exc()
            self.stop()
            sys.exit(-1)
    
    def init_droidbot(self, is_harmonyos):
        # initializer for Android system
        if not is_harmonyos:
            from .app import App
            from .device import Device
            self.app = App(self.app_path, output_dir=self.output_dir, settings=self.settings)
            self.device = Device(
                device_serial=self.device_serial,
                is_emulator=self.is_emulator,
                output_dir=self.output_dir,
                cv_mode=self.cv_mode,
                grant_perm=self.grant_perm,
                send_document=self.send_document,
                enable_accessibility_hard=self.enable_accessibility_hard,
                humanoid=self.humanoid,
                ignore_ad=self.ignore_ad,
                app_package_name=self.app.package_name,
                is_harmonyos=is_harmonyos
            )

            self.env_manager = AppEnvManager(
                device=self.device, app=self.app, env_policy=self.env_policy
            )
            self.input_manager = InputManager(
                device=self.device,
                app=self.app,
                policy_name=self.policy_name,
                random_input=self.random_input,
                event_interval=self.event_interval,
                event_count=self.event_count,
                script_path=self.script_path,
                profiling_method=self.profiling_method,
                master=self.master,
                replay_output=self.replay_output,
                kea=self.kea,
                number_of_events_that_restart_app=self.number_of_events_that_restart_app,
                generate_utg=self.generate_utg
            )
            # self.send_documents()
        # initializer for HarmonyOS system
        else:
            from .device_hm import DeviceHM
            from .app_hm import AppHM
            self.device = DeviceHM(
                    device_serial=self.device_serial,
                    is_emulator=self.is_emulator,
                    output_dir=self.output_dir,
                    cv_mode=self.cv_mode,
                    grant_perm=self.grant_perm,
                    enable_accessibility_hard=self.enable_accessibility_hard,
                    humanoid=self.humanoid,
                    ignore_ad=self.ignore_ad,
                    is_harmonyos=is_harmonyos,
                    save_log=False,
                    settings=self.settings)
            self.app = AppHM(self.app_path, output_dir=self.output_dir, settings=self.settings)

            self.env_manager = AppEnvManager(
                device=self.device,
                app=self.app,
                env_policy=self.env_policy)
            self.input_manager = InputManager(
                device=self.device,
                app=self.app,
                policy_name=self.policy_name,
                random_input=self.random_input,
                event_count=self.event_count,
                event_interval=self.event_interval,
                script_path=self.script_path,
                profiling_method=self.profiling_method,
                master=self.master,
                replay_output=self.replay_output,
                kea=self.kea)

    @staticmethod
    def get_instance():
        if DroidBot.instance is None:
            print("Error: DroidBot is not initiated!")
            sys.exit(-1)
        return DroidBot.instance

    def start(self):
        """
        start interacting
        :return:
        """
        if not self.enabled:
            return
        self.logger.info("Starting DroidBot")
        try:
            if self.timeout > 0:
                self.logger.info("Will stop in %d seconds.", self.timeout)
                self.timer = Timer(self.timeout, self.stop)
                self.timer.start()

            self.device.set_up()

            if not self.enabled:
                return
            self.device.connect()

            if not self.enabled:
                return
            self.device.send_documents(self.app)
            self.device.install_app(self.app)

            if not self.enabled:
                return
            self.env_manager.deploy()

            if not self.enabled:
                return
            if self.droidbox is not None:
                self.droidbox.set_apk(self.app.app_path)
                self.droidbox.start_unblocked()
                self.input_manager.start()
                self.droidbox.stop()
                self.droidbox.get_output()
            else:
                self.input_manager.start()
        except KeyboardInterrupt:
            self.logger.info("Keyboard interrupt.")
            pass
        except Exception:
            import traceback

            traceback.print_exc()
            self.stop()
            sys.exit(-1)

        self.stop()
        self.logger.info("DroidBot Stopped")

    def stop(self):
        self.enabled = False
        if self.timer and self.timer.is_alive():
            self.timer.cancel()
        if self.env_manager:
            self.env_manager.stop()
        if self.input_manager:
            self.input_manager.stop()
        if self.droidbox:
            self.droidbox.stop()
        if self.device:
            self.device.disconnect()
        if not self.keep_env:
            self.device.tear_down()
        if not self.keep_app:
            self.device.uninstall_app(self.app)
        if (
            hasattr(self.input_manager.policy, "master")
            and self.input_manager.policy.master
        ):
            import xmlrpc.client

            proxy = xmlrpc.client.ServerProxy(self.input_manager.policy.master)
            proxy.stop_worker(self.device.serial)

class DroidBotException(Exception):
    pass
