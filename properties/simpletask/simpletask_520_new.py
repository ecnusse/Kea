import sys
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @initialize()
    def set_up(self):
        if d(text="OK").exists():
            d(text="OK").click()

    @main_path()
    def should_keep_scroll_posistion_mainpath(self):
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
    apk_path="./apk/simpletask/11.0.1.apk",
    device_serial="emulator-5554",
    output_dir="../output/simpletask/520/mutate_new",
    policy_name="mutate"
)
run_android_check_as_test(t,setting)

