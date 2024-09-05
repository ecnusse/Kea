import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    
    

    @initialize()
    def set_up(self):
        d(text="Get Started").click()

    @precondition(
        lambda self: d(text="Preview").exists() and
        d(resourceId="com.ichi2.anki:id/preview_next_flashcard").exists() and 
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
    apk_path="./apk/ankidroid/2.18alpha6.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/5688/random_100/1",
    policy_name="random",
    
    number_of_events_that_restart_app = 10
)

