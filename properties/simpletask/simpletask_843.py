import sys
sys.path.append("..")
from kea.core import *

class Test(Kea):
    

    @initializer()
    def set_up(self):
        if d(text="OK").exists():
            d(text="OK").click()

    @mainPath()
    def rotate_device_should_keep_text_mainpath(self):
        d(resourceId="nl.mpcjanssen.simpletask:id/fab").click()
        d(resourceId="nl.mpcjanssen.simpletask:id/taskText").click()
        d.send_keys("Hello World")

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

        


if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/simpletask/10.0.7.apk",
        device_serial="emulator-5554",
        output_dir="../output/simpletask/843/guided",
        policy_name="guided"
    )
    start_kea(t,setting)
    
