import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @precondition(
        lambda self: d(resourceId="com.ichi2.anki:id/fab_expand_menu_button").exists() and 
        d(text="Custom study session").exists() and 
        d(resourceId="com.ichi2.anki:id/action_sync").exists() and not
        d(text="Card browser").exists() 
    )
    @rule()
    def rename_dialog_shouldnot_hide(self):
        d(text="Custom study session").long_click()
        
        d(text="Custom study").click()
        
        d(text="Review ahead").click()
        
        d(text="OK").click()
        

        assert d(text="Rename the existing custom study deck first").exists(), "rename dialog should not hide"



t = Test()

setting = Setting(
    apk_path="./apk/ankidroid/2.13.5.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/7680/mutate/1",
    policy_name="random",

    main_path="main_path/ankidroid/7680.json"
)
start_kea(t,setting)

