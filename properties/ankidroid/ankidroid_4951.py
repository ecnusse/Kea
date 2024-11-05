import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    
    @precondition(
        lambda self: d(text="AnkiDroid").exists() and
        d(resourceId="com.ichi2.anki:id/fab_expand_menu_button").exists() and 
        d(resourceId="com.ichi2.anki:id/deckpicker_name").exists()
    )
    @rule()
    def rule_allow_permission_three_points_exists(self):
        
        assert d(description="More options").exists()
        


t = Test()

setting = Setting(
    apk_path="./apk/ankidroid/2.9alpha29.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/4951/mutate/1",
    policy_name="random",

    grant_perm=False,
    main_path="main_path/ankidroid/4951.json"
)
start_kea(t,setting)

