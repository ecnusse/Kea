import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
     
    @initialize()
    def set_up(self):
        d(text="Get Started").click()    
    # 4935
    @precondition(
        lambda self: d(text="General").exists() and
        d(text="Appearance").exists()
        )
    @rule()
    def back_should_navigate_to_last_page(self):
        d(text="Appearance").click()
        
        d.press("back")
        
        assert d(text="General").exists()
        


t = Test()

setting = Setting(
    apk_path="./apk/ankidroid/2.18alpha6.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/4935/mutate_new/1",
    policy_name="random",

    main_path="main_path/ankidroid/4935_new.json"
)
run_android_check_as_test(t,setting)

