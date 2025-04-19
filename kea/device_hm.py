import json
import logging
import os
import re
import subprocess
import sys
import time
from typing import IO
import typing

if typing.TYPE_CHECKING:
    from .start import Setting
from .input_event import InputEvent, TouchEvent, LongTouchEvent, ScrollEvent, SetTextEvent, KeyEvent

from .device import Device
from .adapter.hdc import HDC, HDC_EXEC
from .app_hm import AppHM
from .adapter.hilog import Hilog
from .intent import Intent

DEFAULT_NUM = '1234567890'
DEFAULT_CONTENT = 'Hello world!'


class DeviceHM(Device):
    """
    this class describes a connected device
    """

    def __init__(self, device_serial=None, is_emulator=False, output_dir=None,
                 cv_mode=False, grant_perm=False, telnet_auth_token=None,
                 enable_accessibility_hard=False, humanoid=None, ignore_ad=False, 
                 is_harmonyos=True, save_log=False, settings:"Setting"=None):
        """
        initialize a device connection
        :param device_serial: serial number of target device
        :param is_emulator: boolean, type of device, True for emulator, False for real device
        :return:
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.cur_event_count = 0
        self.screenshot_path = None
        self.current_state = None

        if "emulator" in device_serial and not is_emulator:
            self.logger.warning("Seems like you are using an emulator. If so, please add is_emulator option.")
        self.serial = device_serial
        self.is_emulator = is_emulator
        self.cv_mode = cv_mode
        self.output_dir = output_dir
        if output_dir is not None:
            if not os.path.isdir(output_dir):
                os.makedirs(output_dir)
        self.grant_perm = grant_perm
        self.enable_accessibility_hard = enable_accessibility_hard
        self.humanoid = humanoid
        self.ignore_ad = ignore_ad

        # basic device information
        self.settings = settings
        self.display_info = None
        self._model_number = None
        self._device_name = None
        self.sdk_version = None
        self.release_version = None
        self.connected = True
        self.last_know_state = None
        self.__used_ports = []
        self.pause_sending_event = False

        self.is_harmonyos = is_harmonyos
        self.save_log = save_log


        from hmdriver2.driver import Driver
        self.hm2 = Driver(serial=self.serial)

        # adapters
        self.hdc = HDC(device=self, hmclient=self.hm2)
        self.hilog = Hilog(device=self)

        self.logger.info("You're runing droidbot on HarmonyOS")
        self.adapters = {
            self.hdc: True,
            self.hilog: True if self.save_log else False
        }

    def check_connectivity(self):
        """
        check if the device is available
        """
        for adapter in self.adapters:
            adapter_name = adapter.__class__.__name__
            adapter_enabled = self.adapters[adapter]
            if not adapter_enabled:
                print("[CONNECTION] %s is not enabled." % adapter_name)
            else:
                if adapter.check_connectivity():
                    print("[CONNECTION] %s is enabled and connected." % adapter_name)
                else:
                    print("[CONNECTION] %s is enabled but not connected." % adapter_name)

    def set_up(self):
        """
        Set connections on this device
        """
        # wait for emulator to start
        # self.wait_for_device()
        for adapter in self.adapters:
            adapter_enabled = self.adapters[adapter]
            if not adapter_enabled:
                continue
            adapter.set_up()

    def connect(self):
        """
        establish connections on this device
        :return:
        """
        for adapter in self.adapters:
            adapter_enabled = self.adapters[adapter]
            if not adapter_enabled:
                continue
            adapter.connect()

        # self.get_sdk_version()
        # self.get_release_version()
        # self.get_ro_secure()
        # self.get_ro_debuggable()
        # self.get_display_info()

        self.unlock()
        self.check_connectivity()
        self.connected = True

    def disconnect(self):
        """
        disconnect current device
        :return:
        """
        self.connected = False
        for adapter in self.adapters:
            adapter_enabled = self.adapters[adapter]
            if not adapter_enabled:
                continue
            adapter.disconnect()

        if self.output_dir is not None:
            temp_dir = os.path.join(self.output_dir, "temp")
            if os.path.exists(temp_dir):
                import shutil
                shutil.rmtree(temp_dir)

    def tear_down(self):
        for adapter in self.adapters:
            adapter_enabled = self.adapters[adapter]
            if not adapter_enabled:
                continue
            adapter.tear_down()
    
    def send_documents(self, app):
        self.logger.warning("send_documents Not implemented")

    def is_foreground(self, app) -> bool:
        """
        check if app is in foreground of device
        :param app: App
        :return: boolean
        """
        if isinstance(app, str):
            package_name = app
        elif isinstance(app, AppHM):
            package_name = app.get_package_name()
        else:
            return False

        top_activity_name = self.get_top_activity_name()
        if top_activity_name is None:
            return False
        return top_activity_name.startswith(package_name)

    @property
    def model_number(self):
        """
        Get model number
        """
        if self._model_number is None:
            self._model_number = self.hdc.get_model_number()
        return self._model_number
    
    @property
    def device_name(self):
        if self._device_name is None:
            self._device_name = self.hdc.get_device_name()
        return self._device_name

    def get_sdk_version(self):
        pass

    def get_release_version(self):
        """
        Get version of current SDK
        """
        if self.release_version is None:
            self.release_version = self.hdc.get_release_version()
        return self.release_version

    def get_ro_secure(self):
        pass

    def get_ro_debuggable(self):
        pass

    def get_display_info(self, refresh=True):
        """
        get device display information, including width, height, and density
        :param refresh: if set to True, refresh the display info instead of using the old values
        :return: dict, display_info
        """
        r = self.hdc.shell("hidumper -s RenderService -a screen")
        pattern = r"activeMode: (?P<width>\d+)x(?P<height>\d+)"
        m = re.search(pattern, r)
        assert m, "Failed when getting screen resolution with hidumper"
        display_info = {"width":int(m.group("width")), "height":int(m.group("height"))}
        return display_info

    def get_width(self, refresh=False):
        display_info = self.get_display_info(refresh=refresh)
        width = 0
        if "width" in display_info:
            width = display_info["width"]
        elif not refresh:
            width = self.get_width(refresh=True)
        else:
            self.logger.warning("get_width: width not in display_info")
        return width

    def get_height(self, refresh=False):
        display_info = self.get_display_info(refresh=refresh)
        height = 0
        if "height" in display_info:
            height = display_info["height"]
        elif not refresh:
            height = self.get_width(refresh=True)
        else:
            self.logger.warning("get_height: height not in display_info")
        return height

    def unlock(self):
        """
        unlock screen
        skip first-use tutorials
        etc
        :return:
        """
        self.hdc.unlock()

    def send_intent(self, intent):
        """
        send an intent to device via am (ActivityManager)
        :param intent: instance of Intent or str
        :return:
        """
        assert self.hdc is not None
        assert intent is not None
        if isinstance(intent, Intent):
            cmd = intent.get_cmd()
        else:
            cmd = intent
        return self.hdc.shell(cmd)

    def send_event(self, event:"InputEvent"):
        """
        send one event to device
        :param event: the event to be sent
        :return:
        """
        event.send(self)

    def start_app(self, app):
        """
        start an app on the device
        :param app: instance of App, or str of package name
        :return:
        """
        if isinstance(app, str):
            package_name = app
        elif isinstance(app, AppHM):
            package_name = app.get_package_name()
            if app.get_main_activity():
                package_name += "/%s" % app.get_main_activity()
        else:
            self.logger.warning("unsupported param " + app + " with type: ", type(app))
            return
        intent = Intent(suffix=package_name)
        self.send_intent(intent)

    def get_top_activity_name(self) -> str:
        """
        Get current activity
        """
        r = self.hdc.shell("aa dump --mission-list")

        if r"#FOREGROUND" not in r:
            return None
        
        mission_list = r.split("Mission ID")
        for mission in mission_list:
            if "state" not in mission:
                continue
            if "#BACKGROUND" in mission:
                continue
            
            import re
            pattern = r"mission name #\[#(?P<bundleName>.+?):.+?:(?P<abilityName>.+?)\]"
            m = re.search(pattern, mission)
            if m:
                return m.group("bundleName") + "/" + m.group("abilityName")
        
        return None

    def get_current_activity_stack(self):
        """
        Get current activity stack
        :return: a list of str, each str is an activity name, the first is the top activity name
        """
        task_to_activities = self.get_task_activities()
        top_activity = self.get_top_activity_name()
        if top_activity:
            for task_id in task_to_activities:
                activities = task_to_activities[task_id]
                if len(activities) > 0 and activities[0] == top_activity:
                    return activities
            self.logger.warning("Unable to get current activity stack.")
            return [top_activity]
        else:
            return None


    def install_app(self, app):
        """
        install an app to device
        @param app: instance of App
        @return:
        """
        assert isinstance(app, AppHM)
        package_name = app.get_package_name()
        if package_name not in self.hdc.get_installed_apps():
            install_cmd = [HDC_EXEC, "-t", self.serial, "install", "-r"]
            install_cmd.append(HDC.get_relative_path(app.app_path))
            install_p = subprocess.Popen(install_cmd, stdout=subprocess.PIPE)
            # print(" ".join(install_cmd))

            print("Please wait while installing the app...")
            output = install_p.stdout.readline()
            if output:
                print(output.strip().decode())

            if not self.connected:
                install_p.terminate()
                return
        # dump the package info through the bundleName
        # hdc shell bm dump -n [bundleName]
        dumpsys_p = subprocess.Popen([HDC_EXEC, "-t", self.serial, "shell",
                                      "bm","dump" ,"-n", package_name], stdout=subprocess.PIPE)
        dumpsys_lines = []
        while True:
            line = dumpsys_p.stdout.readline()
            if not line:
                break
            if not isinstance(line, str):
                line = line.decode()
            dumpsys_lines.append(line)

        if self.output_dir is not None:
            package_info_file_name = "%s/dumpsys_package_%s.txt" % (self.output_dir, app.get_package_name())
            with open(package_info_file_name, "w") as fp:
                fp.writelines(dumpsys_lines)
        
        with open(package_info_file_name, "r") as fp:
            app.dumpsys_main_activity = self.__parse_main_activity_from_dumpsys_lines(fp)

        self.logger.info("App installed: %s" % package_name)
        self.logger.info("Main activity: %s" % app.get_main_activity())

    @staticmethod
    def __parse_main_activity_from_dumpsys_lines(fp:IO):
        """
        """

        # jump the fist line (the bundleName, which dosen't follow the json format)
        # to correctly parse the file into json
        cur_package = fp.readline().replace(":", "").strip()

        import json
        dumpsys = json.load(fp)

        # main ability
        return dumpsys["hapModuleInfos"][0]["mainAbility"]

    def uninstall_app(self, app):
        """
        Uninstall an app from device.
        :param app: an instance of App or a package name
        """
        if isinstance(app, AppHM):
            package_name = app.get_package_name()
            # if self.settings.is_package:
            #     return
        else:
            package_name = app
        if package_name in self.hdc.get_installed_apps():
            uninstall_cmd = [HDC_EXEC, "-t", self.serial, "uninstall", package_name]
            uninstall_p = subprocess.Popen(uninstall_cmd, stdout=subprocess.PIPE)
            while package_name in self.hdc.get_installed_apps():
                print("Please wait while uninstalling the app...")
                time.sleep(2)
            uninstall_p.terminate()

    def push_file(self, local_file, remote_dir="/sdcard/"):
        """
        push file/directory to target_dir
        :param local_file: path to file/directory in host machine
        :param remote_dir: path to target directory in device
        :return:
        """
        if not os.path.exists(local_file):
            self.logger.warning("push_file file does not exist: %s" % local_file)
        self.hdc.run_cmd(["file send", local_file, remote_dir])

    def pull_file(self, remote_file, local_file):
        r = self.hdc.run_cmd(["file", "recv", remote_file, local_file])
        assert not r.startswith("[Fail]"), "Error with receiving file"

    def take_screenshot(self):
        
        if self.output_dir is None:
            return None

        r = self.hdc.shell("snapshot_display")
        assert "success" in r, "Error when taking screenshot"

        remote_path = r.splitlines()[0].split()[-1]
        file_name = os.path.basename(remote_path)
        temp_path = os.path.join(self.output_dir, "temp")
        local_path = os.path.join(os.getcwd(), temp_path, file_name)

        self.pull_file(remote_path, HDC.get_relative_path(local_path))

        return local_path

    def save_screenshot_for_report(self, event_name=None, event=None, current_state=None):
        """
        save screenshot for report, save to "all_states" dir
        """

        self.cur_event_count += 1
        if current_state is None:
            self.current_state = self.get_current_state()
        else:
            self.current_state = current_state
        self.save_to_all_states_dir(self.screenshot_path, event_name=event_name, event=event)
    
    def draw_event(self, event, event_name, screenshot_path):
        import cv2
        image = cv2.imread(screenshot_path)
        if event is not None and screenshot_path is not None:
            if isinstance(event, InputEvent):
                if isinstance(event, TouchEvent):
                    cv2.rectangle(image, (int(event.view['bounds'][0][0]), int(event.view['bounds'][0][1])),
                                  (int(event.view['bounds'][1][0]), int(event.view['bounds'][1][1])), (0, 0, 255), 5)
                elif isinstance(event, LongTouchEvent):
                    cv2.rectangle(image, (int(event.view['bounds'][0][0]), int(event.view['bounds'][0][1])),
                                  (int(event.view['bounds'][1][0]), int(event.view['bounds'][1][1])), (0, 255, 0), 5)
                elif isinstance(event, SetTextEvent):
                    cv2.rectangle(image, (int(event.view['bounds'][0][0]), int(event.view['bounds'][0][1])),
                                  (int(event.view['bounds'][1][0]), int(event.view['bounds'][1][1])), (255, 0, 0), 5)
                elif isinstance(event, ScrollEvent):
                    cv2.rectangle(image, (int(event.view['bounds'][0][0]), int(event.view['bounds'][0][1])),
                                  (int(event.view['bounds'][1][0]), int(event.view['bounds'][1][1])), (255, 255, 0), 5)
                elif isinstance(event, KeyEvent):
                    cv2.putText(image, event.name, (100, 300), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 255, 0), 3, cv2.LINE_AA)
                else:
                    return
            else:
                if event_name == "click":
                    cv2.rectangle(image, (int(event.bounds.left), int(event.bounds.top)), (int(event.bounds.right), int(event.bounds.bottom)), (0, 0, 255), 5)
                elif event_name == "long_click":
                    cv2.rectangle(image, (int(event.bounds.left), int(event.bounds.top)), (int(event.bounds.right), int(event.bounds.bottom)), (0, 255, 0), 5)
                elif event_name == "set_text":
                    cv2.rectangle(image, (int(event.bounds.left), int(event.bounds.top)), (int(event.bounds.right), int(event.bounds.bottom)), (255, 0, 0), 5)
                elif event_name == "press":
                    cv2.putText(image,event, (100,300), cv2.FONT_HERSHEY_SIMPLEX, 5,(0, 255, 0), 3, cv2.LINE_AA)
                else:
                    return
            try:
                cv2.imwrite(screenshot_path, image)
            except Exception as e:
                self.logger.warning(e)

    def save_to_all_states_dir(self, local_image_path, event, event_name = None):
        import shutil
        all_states_dir = os.path.join(self.output_dir, "all_states")
        if not os.path.exists(all_states_dir):
            os.makedirs(all_states_dir)

        json_dir = os.path.join(self.output_dir, "report_screenshot.json")
        if not self.is_harmonyos:
            if self.adapters[self.minicap]:
                dest_screenshot_path = "%s/screen_%s.jpg" % (all_states_dir, self.cur_event_count)
            else:
                dest_screenshot_path = "%s/screen_%s.png" % (all_states_dir, self.cur_event_count)
        else:
            dest_screenshot_path = "%s/screen_%s.jpeg" % (all_states_dir, self.cur_event_count)

        if self.current_state is not None:
            dest_state_json_path = "%s/state_%s.json" % (all_states_dir, self.cur_event_count)
            state_json_file = open(dest_state_json_path, "w")
            state_json_file.write(self.current_state.to_json())
            state_json_file.close()

        try:
            with open(json_dir, 'r') as json_file:
                report_screens = json.load(json_file)
        except FileNotFoundError:
            report_screens = []
        if event_name is None:
            event_name = event.get_event_name()

        img_file_name = os.path.basename(dest_screenshot_path)

        report_screen = {
            "event": event_name,
            "event_index": str(self.cur_event_count),
            "screen_shoot": img_file_name
        }

        report_screens.append(report_screen)
        with open(json_dir, 'w') as json_file:
            json.dump(report_screens, json_file, indent=4)
        if self.current_state is not None and local_image_path != dest_screenshot_path:
            self.current_state.screenshot_path = dest_screenshot_path
            shutil.move(local_image_path, dest_screenshot_path)

        self.draw_event(event, event_name, dest_screenshot_path)

    def get_current_state(self, action_count=None):
        self.logger.debug("getting current device state...")
        current_state = None
        try:
            foreground_activity = self.get_top_activity_name()
            # activity_stack = self.get_current_activity_stack()
            activity_stack = [foreground_activity]
            # background_services = self.get_service_names()
            screenshot_path = self.take_screenshot()
            self.screenshot_path = screenshot_path
            self.logger.debug("finish getting current device state...")
            # if there's no foreground activities (In home or lock screen)
            views = self.get_views() if foreground_activity is not None else []
            from .device_state import DeviceState
            current_state = DeviceState(self,
                                        views=views,
                                        foreground_activity=foreground_activity,
                                        activity_stack=activity_stack,
                                        background_services=None,
                                        screenshot_path=screenshot_path,
                                        tag=action_count)
        except Exception as e:
            self.logger.warning("exception in get_current_state: %s" % e)
            import traceback
            traceback.print_exc()
        self.logger.debug("finish getting current device state...")
        self.last_know_state = current_state
        if not current_state:
            self.logger.warning("Failed to get current state!")
        return current_state

    def get_last_known_state(self):
        return self.last_know_state

    def view_touch(self, x, y):
        self.hdc.touch(x, y)

    def view_long_touch(self, x, y, duration=2000):
        """
        Long touches at (x, y)
        @param duration: duration in ms
        """
        self.hdc.long_touch(x, y, duration)

    def view_drag(self, start_xy, end_xy, duration):
        """
        Sends drag event n PX (actually it's using C{input swipe} command.
        """
        self.hdc.drag(start_xy, end_xy, duration)

    def view_append_text(self, text):
        try:
            self.hm2.input_text()
        except:
            self.hdc.type(text)

    def view_set_text(self, text):
        try:
            self.hm2.input_text(text) 
        except:
            self.logger.warning(
                "Failed to input text with hmdriver2. Use `hdc` to append text instead."
            )
            self.hdc.type(text)

    def key_press(self, key_code):
        self.hdc.press(key_code)

    def shutdown(self):
        pass
        # self.adb.shell("reboot -p")

    # def get_views(self):
    #     if self.hdc:
    #         views = self.get_views()
    #         if views:
    #             return views
    #         else:
    #             self.logger.warning("Failed to get views using HDC.")

    #     self.logger.warning("failed to get current views!")
    #     return None

    def get_views(self):
        return self.hdc.get_views(self.output_dir)

    def get_random_port(self):
        """
        get a random port on host machine to establish connection
        :return: a port number
        """
        import socket
        temp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        temp_sock.bind(("", 0))
        port = temp_sock.getsockname()[1]
        temp_sock.close()
        if port in self.__used_ports:
            return self.get_random_port()
        self.__used_ports.append(port)
        return port
