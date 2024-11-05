import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    
    

    @precondition(
        lambda self: d(resourceId="com.ichi2.anki:id/card_sfld").exists() and
        d(resourceId="com.ichi2.anki:id/action_search").exists()
    )
    @rule()
    def only_new_card_can_be_reposition(self):
        d(resourceId="com.ichi2.anki:id/action_search").click()
        
        d(resourceId="com.ichi2.anki:id/search_src_text").set_text("is:learn")
        
        d.set_fastinput_ime(False) #
        d.send_action("search") # 
        
        if not d(resourceId="com.ichi2.anki:id/card_sfld").exists():
            print("no learned card found")
            return
        d(resourceId="com.ichi2.anki:id/card_sfld").long_click()
        
        d(description="More options").click()
        
        d(text="Reposition").click()
        
        assert not d(text="Reposition new card").exists(), "Reposition new card found"
        





t = Test()

setting = Setting(
    apk_path="./apk/ankidroid/2.9alpha58.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/5216/mutate/1",
    policy_name="random",

    main_path="main_path/ankidroid/5216.json"
)
start_kea(t,setting)

