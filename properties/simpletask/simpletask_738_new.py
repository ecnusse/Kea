import sys
sys.path.append("..")
from kea.core import *

class Test(Kea):
    
    @initializer()
    def set_up(self):
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

        



if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/simpletask/11.0.1.apk",
        device_serial="emulator-5554",
        output_dir="../output/simpletask/guided_new",
        policy_name="guided"
    )
    start_kea(t,setting)
    
