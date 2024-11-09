import sys
sys.path.append("..")
from kea.main import *

class Test(Kea):

    @mainPath()
    def delete_activity_mainpath(self):
        d(description="Open Navigation").click()
        d(text="Edit Activities").click()
        d(resourceId="de.rampro.activitydiary.debug:id/action_add_activity").click()
        d(resourceId="de.rampro.activitydiary.debug:id/edit_activity_name").set_text("Hello")
        d(resourceId="de.rampro.activitydiary.debug:id/action_edit_done").click()
        d(text="Hello").long_click()
        d(resourceId="de.rampro.activitydiary.debug:id/action_edit_delete").click()
        d(resourceId="de.rampro.activitydiary.debug:id/action_add_activity").click()
        d(resourceId="de.rampro.activitydiary.debug:id/edit_activity_name").set_text("Hello")

    @precondition(
        lambda self: d(text="New Activity").exists() and 
        d(resourceId="de.rampro.activitydiary.debug:id/edit_activity_name").exists() and
        d(resourceId="de.rampro.activitydiary.debug:id/textinput_error").exists()
    )
    @rule()
    def new_activity_name(self):
        name = d(resourceId="de.rampro.activitydiary.debug:id/edit_activity_name").get_text()
        print(name)
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

