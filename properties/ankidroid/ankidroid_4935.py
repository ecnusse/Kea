import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    
       

    @precondition(
        lambda self: d(text="Day theme").exists() and
        d(text="Appearance").exists()
        )
    @rule()
    def back_should_navigate_to_last_page(self):
        d.press("back")
        
        assert d(text="Appearance").exists()
        


t = Test()

setting = Setting(
    apk_path="./apk/ankidroid/2.9alpha29.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/4935/random/1",
    policy_name="random",

    main_path="main_path/ankidroid/4935.json"
)
start_kea(t,setting)

