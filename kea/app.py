import logging
import re  
import os
import hashlib
import subprocess
from .intent import Intent

from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from .core import Setting

class App(object):
    """
    this class describes an app
    """

    def __init__(self, app_path, output_dir=None, settings:"Setting" = None):
        """
        create an App instance
        :param app_path: local file path of app
        :return:
        """
        assert app_path is not None
        self.logger = logging.getLogger(self.__class__.__name__)

        self.output_dir = output_dir
        if output_dir is not None:
            if not os.path.isdir(output_dir):
                os.makedirs(output_dir)

        self.settings = settings

        if not self.settings.is_package:
            self._apk_init(app_path)
        else:    
            self._package_init(package_name=app_path)

    def _apk_init(self, app_path):
        self.app_path = app_path

        from loguru import logger

        # Disable the logging of the androguard module.
        logger.disable("androguard")
        from androguard.core.apk import APK
        self.apk = APK(self.app_path)
        self.package_name = self.apk.get_package()
        #Used to get the main activity of the APK (i.e., the first activity that launches when the application starts).
        self.main_activity = self.apk.get_main_activity()
        #Get the list of permissions for the application from the self.apk object.
        self.permissions = self.apk.get_permissions()
        #Get the list of activities from the self.apk object.
        self.activities = self.apk.get_activities()
        self.possible_broadcasts = self.get_possible_broadcasts()
        self.hashes = self.get_hashes()    

    def _package_init(self, package_name):
        self.app_path = None
        self.apk = None
        self.package_name = package_name
        self.main_activity = self.dumpsys_main_activity
        # TODO figure out how to get all activities from package name
        self.activities = []
        # TODO parse self.permissions from dumpsys_package_info 

    def get_package_name(self):
        """
        get package name of current app
        :return:
        """
        return self.package_name

    def get_main_activity(self):
        """
        get package name of current app
        :return:
        """
        if self.main_activity is not None:
            return self.main_activity
        else:
            self.logger.warning("Cannot get main activity from manifest. Using dumpsys result instead.")
            return self.dumpsys_main_activity
    
    @property
    def dumpsys_package_info(self):
        cmd = ["adb", "-s", self.settings.device_serial, "shell", "dumpsys", "package", self.package_name]
        output = subprocess.check_output(cmd, text=True)
        return output
    
    def dumpsys_activities(self) -> List: 
        match = re.search(r'android.intent.action.MAIN:\s+.*?/(.*?)\s+filter', self.dumpsys_package_info, re.DOTALL)
        if match:
            return match.group(1)
        else:
            return None
    
    @property
    def dumpsys_main_activity(self):
        match = re.search(r'android.intent.action.MAIN:\s+.*?/(.*?)\s+filter', self.dumpsys_package_info, re.DOTALL)
        if match:
            return match.group(1)
        else:
            return None 

    def get_start_intent(self):
        """
        get an intent to start the app
        :return: Intent
        """
        package_name = self.get_package_name()
        if self.get_main_activity():
            package_name += "/%s" % self.get_main_activity()
        return Intent(suffix=package_name)

    def get_start_with_profiling_intent(self, trace_file, sampling=None):
        """
        get an intent to start the app with profiling
        :return: Intent
        """
        package_name = self.get_package_name()
        if self.get_main_activity():
            package_name += "/%s" % self.get_main_activity()
        if sampling is not None:
            return Intent(prefix="start --start-profiler %s --sampling %d" % (trace_file, sampling), suffix=package_name)
        else:
            return Intent(prefix="start --start-profiler %s" % trace_file, suffix=package_name)

    def get_stop_intent(self):
        """
        get an intent to stop the app
        :return: Intent
        """
        package_name = self.get_package_name()
        return Intent(prefix="force-stop", suffix=package_name)

    def get_possible_broadcasts(self):
        possible_broadcasts = set()
        for receiver in self.apk.get_receivers():
            intent_filters = self.apk.get_intent_filters('receiver', receiver)
            actions = intent_filters['action'] if 'action' in intent_filters else []
            categories = intent_filters['category'] if 'category' in intent_filters else []
            categories.append(None)
            for action in actions:
                for category in categories:
                    intent = Intent(prefix='broadcast', action=action, category=category)
                    possible_broadcasts.add(intent)
        return possible_broadcasts

    def get_hashes(self, block_size=2 ** 8):
        """
        Calculate MD5,SHA-1, SHA-256
        hashes of APK input file
        @param block_size:
        """
        md5 = hashlib.md5()
        sha1 = hashlib.sha1()
        sha256 = hashlib.sha256()
        f = open(self.app_path, 'rb')
        while True:
            data = f.read(block_size)
            if not data:
                break
            md5.update(data)
            sha1.update(data)
            sha256.update(data)
        return [md5.hexdigest(), sha1.hexdigest(), sha256.hexdigest()]
