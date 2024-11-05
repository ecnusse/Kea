import string
import sys
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @initialize()
    def set_up(self):
        if d(text="OK").exists():
            d(text="OK").click()

    @main_path()
    def add_tag_mainpath(self):
        d(resourceId="nl.mpcjanssen.simpletask:id/fab").click()
        d(resourceId="nl.mpcjanssen.simpletask:id/btnProject").click()

    @precondition(
        lambda self: d(resourceId="nl.mpcjanssen.simpletask:id/alertTitle",text="Tag").exists() and 
        d(text="OK").exists() and 
        d(text="CANCEL").exists() 
    )
    @rule()
    def add_tag(self):   
        tag_name = st.text(alphabet=string.ascii_letters,min_size=1, max_size=6).example()
        print("tag name: "+str(tag_name))
        d(resourceId="nl.mpcjanssen.simpletask:id/new_item_text").set_text(tag_name)
        
        d.set_fastinput_ime(False)
        
        # d(description="Done").click()
        
        d(text="OK").click()
        
        content = d(resourceId="nl.mpcjanssen.simpletask:id/taskText").get_text()
        print("content: "+str(content))
        
        assert tag_name in content



t = Test()

setting = Setting(
    apk_path="./apk/simpletask/10.1.15.apk",
    device_serial="emulator-5554",
    output_dir="../output/simpletask/907/mutate",
    policy_name="mutate"
)
run_android_check_as_test(t,setting)

