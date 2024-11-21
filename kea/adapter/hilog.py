import subprocess
import logging
import threading
from .hdc import HDC_EXEC, HDC

class Hilog:
    def __init__(self, device=None):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.device = device
        self.connected = False
        self.process = None
        self.recent_lines = []
        if device.output_dir is None:
            self.out_file = None
        else:
            self.out_file = "%s/hilog.txt" % device.output_dir
    
    def set_up(self):
        self.logger.info(f"[CONNECTION] Setting up Adapter hilog")

    def connect(self):
        self.process = subprocess.Popen([HDC_EXEC, "shell", "hilog"],
                                        stdin=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        stdout=subprocess.PIPE)
        self.connected = True
        listen_thread = threading.Thread(target=self.handle_output)
        listen_thread.start()
    
    def check_connectivity(self):
        return self.connected

    def disconnect(self):
        self.connected = False
        if self.process is not None:
            self.process.terminate()

    def handle_output(self):
        f = None
        if self.out_file is not None:
            f = open(self.out_file, 'w', encoding='utf-8')

        while self.connected:
            line = self.process.stdout.readline()
            if not isinstance(line, str):
                line = line.decode()
            self.recent_lines.append(line)
            self.parse_line(line)
            if f is not None:
                f.write(line)
        if f is not None:
            f.close()
        self.logger.info(f"[CONNECTION] Hilog is disconnected")
    
    def tear_down(self):
        pass

    def parse_line(self, hilog_line):
        # 解析逻辑可以在这里实现
        pass

    def get_recent_lines(self):
        lines = self.recent_lines
        self.recent_lines = []
        return lines
