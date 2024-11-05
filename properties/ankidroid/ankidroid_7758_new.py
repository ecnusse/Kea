import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @initialize()
    def set_up(self):
        d(description="Navigate up").click()
        
        d(text="Settings").click()
        
        d(text="AnkiDroid").click()
        
        d(text="Language").click()
        
        d(scrollable=True).scroll.to(text="日本語")
        
        d(text="日本語").click()
        

    @precondition(
        lambda self: d(resourceId="com.ichi2.anki:id/card_sfld").exists() and 
        d(resourceId="com.ichi2.anki:id/action_search").exists() 
    )
    @rule()
    def card_info_should_be_translated(self):
        d(resourceId="com.ichi2.anki:id/card_sfld").long_click()
        
        d(resourceId="com.ichi2.anki:id/toolbar").child(className="android.widget.ImageView").click()
        
        assert not d(text="Card Info").exists(), "Card Info found"




t = Test()

setting = Setting(
    apk_path="./apk/ankidroid/2.18alpha6.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/7758/mutate/1",
    policy_name="random",

    main_path="main_path/ankidroid/7758.json"
)
start_kea(t,setting)

