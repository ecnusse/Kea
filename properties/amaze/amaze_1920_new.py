import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @initialize()
    def set_up(self):
        if d(text="ALLOW").exists():
            d(text="ALLOW").click()
            
        elif d(text="Allow").exists():
            d(text="Allow").click()
            
    # 1920
    @precondition(lambda self: d(text="FTP Server").exists() and d(text="START").exists())
    @rule()
    def should_notice_user_when_no_network(self):
        d(text="START").click()
        
        assert d(text="STOP").exists()




t = Test()

setting = Setting(
    apk_path="./apk/amaze/3.8.4.apk",
    device_serial="emulator-5554",
    output_dir="output/amaze/1920/random_100/1",
    policy_name="random",
    
    number_of_events_that_restart_app = 100
)
start_kea(t,setting)

