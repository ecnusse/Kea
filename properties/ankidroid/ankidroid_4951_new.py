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
        lambda self: d(text="AnkiDroid").exists() and
        d(resourceId="com.ichi2.anki:id/fab_main").exists() and 
        d(resourceId="com.ichi2.anki:id/deckpicker_name").exists()
    )
    @rule()
    def rule_allow_permission_three_points_exists(self):
        
        assert d(description="More options").exists()
        



t = Test()

setting = Setting(
    apk_path="./apk/ankidroid/2.18alpha6.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/4951/mutate_new/1",
    policy_name="random",

    main_path="main_path/ankidroid/4951_new.json"
    
)

