import sys
sys.path.append("..")
from kea.core import *

class Test(Kea):
    

    @initializer()
    def set_up(self):
        if d(text="OK").exists():
            d(text="OK").click()
        
    @mainPath()
    def enter_task_and_back_should_keep_position_mainpath(self):
        d(resourceId="nl.mpcjanssen.simpletask:id/fab").click()
        d(resourceId="nl.mpcjanssen.simpletask:id/taskText").set_text("Hello World!")
        d(resourceId="nl.mpcjanssen.simpletask:id/btnSave").click()
        d(resourceId="nl.mpcjanssen.simpletask:id/fab").click()
        d(resourceId="nl.mpcjanssen.simpletask:id/taskText").set_text("Hello1")
        d(resourceId="nl.mpcjanssen.simpletask:id/btnSave").click()
        d(resourceId="nl.mpcjanssen.simpletask:id/fab").click()
        d(resourceId="nl.mpcjanssen.simpletask:id/taskText").set_text("Hello2")
        d(resourceId="nl.mpcjanssen.simpletask:id/btnSave").click()
        d(resourceId="nl.mpcjanssen.simpletask:id/fab").click()
        d(resourceId="nl.mpcjanssen.simpletask:id/taskText").set_text("Hello3")
        d(resourceId="nl.mpcjanssen.simpletask:id/btnSave").click()
        d(resourceId="nl.mpcjanssen.simpletask:id/fab").click()
        d(resourceId="nl.mpcjanssen.simpletask:id/taskText").set_text("Hello4")
        d(resourceId="nl.mpcjanssen.simpletask:id/btnSave").click()
        d(resourceId="nl.mpcjanssen.simpletask:id/fab").click()
        d(resourceId="nl.mpcjanssen.simpletask:id/taskText").set_text("Hello5")
        d(resourceId="nl.mpcjanssen.simpletask:id/btnSave").click()
        d(resourceId="nl.mpcjanssen.simpletask:id/fab").click()
        d(resourceId="nl.mpcjanssen.simpletask:id/taskText").set_text("Hello6")
        d(resourceId="nl.mpcjanssen.simpletask:id/btnSave").click()
        d(resourceId="nl.mpcjanssen.simpletask:id/fab").click()
        d(resourceId="nl.mpcjanssen.simpletask:id/taskText").set_text("Hello7")
        d(resourceId="nl.mpcjanssen.simpletask:id/btnSave").click()
        d(resourceId="nl.mpcjanssen.simpletask:id/fab").click()
        d(resourceId="nl.mpcjanssen.simpletask:id/taskText").set_text("Hello8")
        d(resourceId="nl.mpcjanssen.simpletask:id/btnSave").click()
        d(resourceId="nl.mpcjanssen.simpletask:id/fab").click()
        d(resourceId="nl.mpcjanssen.simpletask:id/taskText").set_text("Hello9")
        d(resourceId="nl.mpcjanssen.simpletask:id/btnSave").click()
        d(resourceId="nl.mpcjanssen.simpletask:id/fab").click()
        d(resourceId="nl.mpcjanssen.simpletask:id/taskText").set_text("Hello10")
        d(resourceId="nl.mpcjanssen.simpletask:id/btnSave").click()
        d(resourceId="nl.mpcjanssen.simpletask:id/fab").click()
        d(resourceId="nl.mpcjanssen.simpletask:id/taskText").set_text("Hello11")
        d(resourceId="nl.mpcjanssen.simpletask:id/btnSave").click()
        d(resourceId="nl.mpcjanssen.simpletask:id/fab").click()
        d(resourceId="nl.mpcjanssen.simpletask:id/taskText").set_text("Hello12")
        d(resourceId="nl.mpcjanssen.simpletask:id/btnSave").click()
        d(resourceId="nl.mpcjanssen.simpletask:id/fab").click()
        d(resourceId="nl.mpcjanssen.simpletask:id/taskText").set_text("Hello13")
        d(resourceId="nl.mpcjanssen.simpletask:id/btnSave").click()
        d(resourceId="nl.mpcjanssen.simpletask:id/fab").click()
        d(resourceId="nl.mpcjanssen.simpletask:id/taskText").set_text("Hello14")
        d(resourceId="nl.mpcjanssen.simpletask:id/btnSave").click()

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




if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/simpletask/10.2.4.apk",
        device_serial="emulator-5554",
        output_dir="../output/simpletask/941/guided",
        policy_name="guided"
    )
    start_kea(t,setting)
    
