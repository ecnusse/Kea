import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    


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



t = Test()

setting = Setting(
    apk_path="./apk/activitydiary/1.4.2.apk",
    device_serial="emulator-5554",
    output_dir="output/activitydiary/109/1",
    policy_name="random",

)

