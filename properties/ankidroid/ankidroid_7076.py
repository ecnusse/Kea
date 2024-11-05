import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @precondition(
        lambda self: d(text="考研").exists() and d(text="例句").exists() and 
        d(resourceId="com.ichi2.anki:id/action_sync").exists()
    )
    @rule()
    def should_display_name_of_sub_deck(self):
        d(text="考研").click()
        
        assert d(text="例句").exists(), "例句 not found"



t = Test()

setting = Setting(
    apk_path="./apk/ankidroid/2.14alpha1.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/7076/mutate/1",
    policy_name="random",

    main_path="main_path/ankidroid/7076.json"
)
start_kea(t,setting)

