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
            
        if d(text="Saved filters").exists():
            d.press("back")

    @precondition(
        lambda self: int(d(resourceId="nl.mpcjanssen.simpletask:id/tasktext").count) > 0 and not d(text="Quick filter").exists() and not d(text="Settings").exists() and not d(text="Saved filters").exists())
    @rule()
    def save_reopen_task_should_not_change_number(self):
        task_count = int(d(resourceId="nl.mpcjanssen.simpletask:id/tasktext").count)
        print("task count: "+str(task_count))
        selected_task = random.randint(0, task_count - 1)
        print("selected task: "+str(selected_task))
        selected_task = d(resourceId="nl.mpcjanssen.simpletask:id/tasktext")[selected_task]
        selected_task_name = selected_task.get_text()
        print("selected task name: "+str(selected_task_name))
        selected_task.click()
        
        d(resourceId="nl.mpcjanssen.simpletask:id/update").click()
        
        d(resourceId="nl.mpcjanssen.simpletask:id/btnSave").click()
        
        new_count = int(d(resourceId="nl.mpcjanssen.simpletask:id/tasktext").count)
        print("new count: "+str(new_count))
        assert task_count == new_count, "task count should be the same"
    



t = Test()

setting = Setting(
    apk_path="./apk/simpletask/10.3.0.apk",
    device_serial="emulator-5554",
    output_dir="output/simpletask/993/random_100/1",
    policy_name="random",

    main_path="main_path/simpletask/993.json"
)
run_android_check_as_test(t,setting)

