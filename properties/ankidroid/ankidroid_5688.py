import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    
        

    @precondition(
        lambda self: d(text="Preview").exists() and
        d(resourceId="com.ichi2.anki:id/nextTime2").exists() and 
        d(resourceId="qa").exists() and 
        d(resourceId="qa").get_text() != ""
    )
    @rule()
    def rotate_device_should_keep_review_card(self):
        card_content = d(resourceId="qa").get_text()
        print("card_content: " + str(card_content))
        d.set_orientation("l")
        
        d.set_orientation("n")
        
        new_card_content = d(resourceId="qa").get_text()
        print("new_card_content: " + str(new_card_content))
        assert card_content == new_card_content, "card content should not change"




t = Test()

setting = Setting(
    apk_path="./apk/ankidroid/2.9.2.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/5688/mutate/1",
    policy_name="random",

    main_path="main_path/ankidroid/5688.json"
)
run_android_check_as_test(t,setting)

