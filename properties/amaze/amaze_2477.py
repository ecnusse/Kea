import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @initialize()
    def set_up(self):
        if d(text="ALLOW").exists():
            d(text="ALLOW").click()
            
        elif d(text="Allow").exists():
            d(text="Allow").click()
            

    @precondition(lambda self: d(text="Color").exists() and d(text="Customize").exists())
    @rule()
    def back_should_not_go_to_main_setting(self):
        
        d(description="Navigate up").click()
        
        assert not d(text="Settings").exists()
    


t = Test()

setting = Setting(
    apk_path="./apk/amaze/amaze-b7c9c81.apk",
    device_serial="emulator-5554",
    output_dir="output/amaze/2477/mutate/1",
    policy_name="random",

    main_path="main_path/amaze/2477.json"
)
start_kea(t,setting)

