import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    
    

    @precondition(
        lambda self: 
        d(resourceId="com.ichi2.anki:id/new_number").exists() and
        d(resourceId="com.ichi2.anki:id/answer_field").exists() and 
        d(resourceId="com.ichi2.anki:id/answer_field").get_text() != "Type answer" and
        d(resourceId="com.ichi2.anki:id/answer_options_layout").exists()
    )
    @rule()
    def text_should_display_after_type_answer(self):
        typed_text = d(resourceId="com.ichi2.anki:id/answer_field").get_text()
        print("typed_text: " + typed_text)
        d(resourceId="com.ichi2.anki:id/answer_options_layout").click()
        
        for view in d(resourceId="content").child(className="android.view.View"):
            print("view text: " + view.get_text())
            if typed_text in view.get_text():
                return True 
        assert False, "text should display after type answer"



t = Test()

setting = Setting(
    apk_path="./apk/ankidroid/2.8.4.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/5334/random_100/1",
    policy_name="random",
    
    number_of_events_that_restart_app = 100
)
start_kea(t,setting)

