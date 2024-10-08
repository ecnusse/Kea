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
        lambda self: d(resourceId="nl.mpcjanssen.simpletask:id/fab").exists() and 
        d(resourceId="nl.mpcjanssen.simpletask:id/search").exists() and not 
        d(resourceId="nl.mpcjanssen.simpletask:id/filter_text").exists() and not 
        d(text="Quick filter").exists() and not 
        d(text="Settings").exists() and not 
        d(text="Saved filters").exists()
    )
    @rule()
    def click_new_task_should_enter_add_task_instead_of_update(self):
        d(resourceId="nl.mpcjanssen.simpletask:id/fab").click()
        
        assert d(text="Add Task").exists(), "Add Task should exist"
       


t = Test()

setting = Setting(
    apk_path="./apk/simpletask/9.0.1.apk",
    device_serial="emulator-5554",
    output_dir="output/simpletask/738/random_100/1",
    policy_name="random",

    main_path="main_path/simpletask/738.json"
)
run_android_check_as_test(t,setting)

