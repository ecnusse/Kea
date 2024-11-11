import string
import sys
sys.path.append("..")
from kea.main import *

class Test(Kea):

    @mainPath()
    def delete_activity_mainpath(self):
        d(description="Open navigation").click()
        d(text="Edit Activities").click()
        d(resourceId="de.rampro.activitydiary:id/action_add_activity").click()
        d(resourceId="de.rampro.activitydiary:id/edit_activity_name").set_text("Hello")
        d(resourceId="de.rampro.activitydiary:id/action_edit_done").click()
        d(text="Hello").long_click()
        d(resourceId="de.rampro.activitydiary:id/action_edit_delete").click()
        d(resourceId="de.rampro.activitydiary:id/action_add_activity").click()
        d(resourceId="de.rampro.activitydiary:id/edit_activity_name").set_text("Hello")

    @precondition(
        lambda self: d(text="New activity").exists() and d(resourceId="de.rampro.activitydiary:id/edit_activity_name").exists()
    )
    @rule()
    def new_activity_name(self):
        name = st.text(alphabet=string.digits + string.ascii_letters + string.punctuation,min_size=1, max_size=5).example()
        print(name)
        d(resourceId="de.rampro.activitydiary:id/edit_activity_name").set_text(name)
        
        if d(resourceId="de.rampro.activitydiary:id/textinput_error").exists():
            d(description="Navigate up").click()
            
            assert d(resourceId="de.rampro.activitydiary:id/activity_name",text=name).exists() , "activity name not exists"



if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/activitydiary/1.4.0.apk",
        device_serial="emulator-5554",
        output_dir="output/activitydiary/109/1",
        policy_name="random"
    )
    
