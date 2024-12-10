import sys
sys.path.append("..")
from kea import *

class Test(KeaTest):

    @mainPath()
    def Fail_to_send_feedback_mainpath(self):
        d(description="Navigate up").click()
        d(text="Help").click()
        d(text="Get Help").click()
        d(text="Send troubleshooting report").click()

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



if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/ankidroid/2.15alpha34.apk",
        device_serial="emulator-5554",
        output_dir="../output/ankidroid/8379/guided",
        policy_name="guided"
    )
    start_kea(t,setting)
    
