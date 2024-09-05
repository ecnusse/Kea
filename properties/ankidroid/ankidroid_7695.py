import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @precondition(
        lambda self: d(text="Front").exists() and 
        d(text="Rename field").exists()
    )
    @rule()
    def rename_note_type_shouldnot_display(self):
        
        d(text="Rename field").click()
        
        assert not d(text="Rename note type").exists(), "Rename note type found"



t = Test()

setting = Setting(
    apk_path="./apk/ankidroid/2.13.5.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/7695/mutate/1",
    policy_name="random",

    main_path="main_path/ankidroid/7695.json"
)
run_android_check_as_test(t,setting)

