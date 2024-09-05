import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @initialize()
    def set_up(self):
        if d(text="GRANT").exists():
            d(text="GRANT").click()
            
        elif d(text="Grant").exists():
            d(text="Grant").click()
            

        if d(text="ALLOW").exists():
            d(text="ALLOW").click()
            
        elif d(text="Allow").exists():
            d(text="Allow").click()
            

    @precondition(lambda self: d(text="App Manager").exists() and d(description="More options").exists() and not d(text="Settings").exists())
    @rule()
    def click_exist_button_should_work(self):
        
        d(description="More options").click()
        
        d(text="Exit").click()
        
        assert not d(text="App Manager").exists()
    



t = Test()

setting = Setting(
    apk_path="./apk/amaze/amaze-9f3f1dc6c3.apk",
    device_serial="emulator-5554",
    output_dir="output/amaze/2518/mutate/1",
    policy_name="random",

    main_path="main_path/amaze/2518.json"
)
run_android_check_as_test(t,setting)

