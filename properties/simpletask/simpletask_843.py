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
        lambda self: d(text="Add Task").exists() and 
        len(d(resourceId="nl.mpcjanssen.simpletask:id/taskText").get_text())!=121
    )
    @rule()
    def rotate_device_should_keep_text(self):
        content = d(resourceId="nl.mpcjanssen.simpletask:id/taskText").get_text()
        print("content: "+str(content))
        d.set_orientation("l")
        
        d.set_orientation("n")
        
        new_content = d(resourceId="nl.mpcjanssen.simpletask:id/taskText").get_text()
        print("new content: "+str(new_content))
        assert content == new_content

        


t = Test()

setting = Setting(
    apk_path="./apk/simpletask/10.0.7.apk",
    device_serial="emulator-5554",
    output_dir="output/simpletask/843/mutate/1",
    policy_name="random",

    main_path="main_path/simpletask/843.json"
)
start_kea(t,setting)

