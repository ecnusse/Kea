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
        lambda self: int(d(resourceId="nl.mpcjanssen.simpletask:id/tasktext").count) > 13 and not d(text="Settings").exists() and not d(text="Saved filters").exists())
    @rule()
    def enter_task_and_back_should_keep_position(self):
        task_count = int(d(resourceId="nl.mpcjanssen.simpletask:id/tasktext").count)
        print("task count: "+str(task_count))
        selected_task = -1
        print("selected task: "+str(selected_task))
        selected_task = d(resourceId="nl.mpcjanssen.simpletask:id/tasktext")[selected_task]
        selected_task_name = selected_task.get_text()
        print("selected task name: "+str(selected_task_name))
        selected_task.click()
        
        d(resourceId="nl.mpcjanssen.simpletask:id/update").click()
        
        d(resourceId="nl.mpcjanssen.simpletask:id/btnSave").click()
        
        assert d(text=selected_task_name).exists(), "selected_task_name not exists"




t = Test()

setting = Setting(
    apk_path="./apk/simpletask/10.2.4.apk",
    device_serial="emulator-5554",
    output_dir="output/simpletask/941/random_100/1",
    policy_name="random",

    main_path="main_path/simpletask/941.json"
)
start_kea(t,setting)

