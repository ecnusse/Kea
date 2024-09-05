import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @precondition(lambda self: d(text="App Manager").exists() and d(description="More options").exists())
    @rule()
    def click_exist_button_should_work(self):
        
        d(description="More options").click()
        
        d(text="Exit").click()
        
        assert not d(text="App Manager").exists()
    



t = Test()

setting = Setting(
    apk_path="./apk/amaze-3.8.4.apk",
    device_serial="emulator-5554",
    output_dir="output/amaze/2518/1",
    policy_name="random",

)

