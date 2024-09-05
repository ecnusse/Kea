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
        lambda self: int(d(resourceId="nl.mpcjanssen.simpletask:id/tasktext").count) > 12 and not d(resourceId="nl.mpcjanssen.simpletask:id/filter_text").exists() and not d(text="Quick filter").exists() and not d(text="Settings").exists() and not d(text="Saved filters").exists()
    )
    @rule()
    def should_keep_scroll_posistion(self):
        selected_task = d(resourceId="nl.mpcjanssen.simpletask:id/tasktext")[-1].get_text()
        print("selected task: "+str(selected_task))
        d.press("recent")
        
        d.press("back")
        
        assert d(text=selected_task).exists()
        


t = Test()

setting = Setting(
    apk_path="./apk/simpletask/8.2.0.apk",
    device_serial="emulator-5554",
    output_dir="output/simpletask/520/mutate/1",
    policy_name="random",

    main_path="main_path/simpletask/520.json"
)
run_android_check_as_test(t,setting)

