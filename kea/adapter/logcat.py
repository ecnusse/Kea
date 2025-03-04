import subprocess
import logging
import copy
from .adapter import Adapter


class Logcat(Adapter):
    """
    A connection with the target device through logcat.
    """

    def __init__(self, device=None):
        """
        initialize logcat connection
        :param device: a Device instance
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        if device is None:
            from kea.device import Device
            device = Device()
        self.device = device
        self.connected = False
        self.process = None
        self.parsers = []
        self.recent_lines = []
        if device.output_dir is None:
            self.out_file = None
        else:
            self.out_file = "%s/logcat.txt" % device.output_dir

    def connect(self):
        try:
            self.device.adb.run_cmd("logcat -c")
        except Exception as e:
            print("An error occurred in logcat -c:", str(e))
        self.process = subprocess.Popen(["adb", "-s", self.device.serial, "logcat", "-v", "threadtime", "*:I"],
                                        stdin=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        stdout=subprocess.PIPE)
        import threading
        try:
            listen_thread = threading.Thread(target=self.handle_output)
            listen_thread.start()
        except Exception as e:
            print("An error occurred in logcat -c:", str(e))


    def disconnect(self):
        self.connected = False
        if self.process is not None:
            self.process.terminate()

    def check_connectivity(self):
        return self.connected

    def get_recent_lines(self):
        lines = self.recent_lines
        self.recent_lines = []
        return lines

    def handle_output(self):
        self.connected = True

        f = None
        if self.out_file is not None:
            f = open(self.out_file, 'w', encoding='utf-8')

        while self.connected:
            if self.process is None:
                continue
            line = self.process.stdout.readline()
            if not isinstance(line, str):
                try:
                    line = line.decode('utf-8')
                except UnicodeDecodeError:
                    try:
                        line = line.decode('ISO-8859-1')
                    except UnicodeDecodeError:
                        line = line.decode('utf-8', errors='replace')
            self.recent_lines.append(line)
            self.parse_line(line)
            if f is not None:
                f.write(line)
        if f is not None:
            f.close()
        print("[CONNECTION] %s is disconnected" % self.__class__.__name__)

    def parse_line(self, logcat_line):
        for parser in self.parsers:
            parser.parse(logcat_line)

