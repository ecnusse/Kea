import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @precondition(
        lambda self: 
        d(text="AnkiDroid Feedback").exists()
    )
    @rule()
    def Fail_to_send_feedback(self):
        if d(text="Cancel").exists():
            d(text="Cancel").click()
        elif d(text="CANCEL").exists():
            d(text="CANCEL").click()
        
        d(text="Send troubleshooting report").click()
        
        assert d(text="AnkiDroid Feedback").exists(), "Fail to send feedback"



t = Test()

setting = Setting(
    apk_path="./apk/ankidroid/2.15alpha34.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/8379/mutate/1",
    policy_name="random",

    main_path="main_path/ankidroid/8379.json"
)
run_android_check_as_test(t,setting)

