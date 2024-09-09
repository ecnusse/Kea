import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @precondition(
        lambda self: d(text="Activity Diary").exists() and not 
        d(text="<No Activity>").exists() and 
        d(description="Statistics").info["selected"] and not 
        d(text="Settings").exists()
    )
    @rule()
    def click_content_should_enter_diary_entry(self):
        activity_name = d(resourceId="de.rampro.activitydiary:id/activity_name").get_text() 
        d(resourceId="de.rampro.activitydiary:id/duration_label").click()
        
        assert d(text="Diary entry").exists(), "not enter diary entry"
        
        current_activity_name = d(resourceId="de.rampro.activitydiary:id/activity_name").get_text()
        assert current_activity_name == activity_name, "activity name changed from "+ activity_name + " to " + current_activity_name



t = Test()

setting = Setting(
    apk_path="./apk/activitydiary/1.4.0.apk",
    device_serial="emulator-5554",
    output_dir="output/activitydiary/253/mutate/1",
    policy_name="random",

    main_path="main_path/activitydiary/253.json"
)
run_android_check_as_test(t,setting)
