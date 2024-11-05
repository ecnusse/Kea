import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @initialize()
    def set_up(self):
        if d(text="OK").exists():
            d(text="OK").click()
        

    @precondition(
        lambda self: d(text="Share").exists() and d(text="Settings").exists()
    )
    @rule()
    def click_share_should_work(self):
        d(text="Share").click()
        
        assert d(text="Save to Drive").exists()
        


t = Test()

setting = Setting(
    apk_path="./apk/simpletask/8.2.0.apk",
    device_serial="emulator-5554",
    output_dir="output/simpletask/538/mutate/1",
    policy_name="random",

    main_path="main_path/simpletask/538.json"
)
start_kea(t,setting)

