import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    
    @precondition(
        lambda self: 
        d(resourceId="com.ichi2.anki:id/card_sfld").exists() and
        d(resourceId="com.ichi2.anki:id/dropdown_deck_name").exists() 
    )
    @rule()
    def reposition_should_not_be_missing(self):
        random_select_card = random.choice(d(resourceId="com.ichi2.anki:id/card_sfld"))
        random_select_card.long_click()
        
        d(description="More options").click()
        
        d(text="Reposition").click()
        
        d(resourceId="com.ichi2.anki:id/dialog_text_input").set_text("1")
        
        d(resourceId="android:id/button1").click()
        
        # go to "more" and check
        d(description="More options").click()
        
        assert d(text="Undo reposition").exists(), "missing Undo reposition"




t = Test()

setting = Setting(
    apk_path="./apk/ankidroid/2.13.5.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/7674/mutate/1",
    policy_name="random",

    main_path="main_path/ankidroid/7674_new.json"
)
run_android_check_as_test(t,setting)

