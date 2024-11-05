import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    
    # 2477
    @precondition(lambda self: d(text="Color").exists() and d(text="Customize").exists())
    @rule()
    def back_should_not_go_to_main_setting(self):
        
        d.press("back")
        
        assert not d(text="Appearance").exists()
    



t = Test()

setting = Setting(
    apk_path="./apk/amaze-3.8.4.apk",
    device_serial="emulator-5554",
    output_dir="output/amaze/2477/1",
    policy_name="random",

    main_path="main_path/amaze/2477.json"
)
start_kea(t,setting)

