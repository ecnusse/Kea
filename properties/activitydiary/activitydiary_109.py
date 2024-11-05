import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    


    @precondition(
        lambda self: d(text="New Activity").exists() and 
        d(resourceId="de.rampro.activitydiary.debug:id/edit_activity_name").exists() and 
        d(resourceId="de.rampro.activitydiary.debug:id/textinput_error").exists()
    )
    @rule()
    def new_activity_name(self):
        name = d(resourceId="de.rampro.activitydiary.debug:id/edit_activity_name").get_text()
        
        d(description="Navigate up").click()
        
        assert d(resourceId="de.rampro.activitydiary.debug:id/activity_name",text=name).exists() , "activity name not exists"



t = Test()

setting = Setting(
    apk_path="./apk/activitydiary/1.1.8.apk",
    device_serial="emulator-5554",
    output_dir="output/activitydiary/109/random_100/1",
    policy_name="random",
    
    number_of_events_that_restart_app = 100
)
start_kea(t,setting)

