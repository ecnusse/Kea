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
        lambda self: d(text="Quick filter").exists() and d(text="CLEAR FILTER").exists() and d(resourceId="android:id/text1",className="android.widget.CheckedTextView").exists()
    )
    @rule()
    def filter_by_tag(self):
        d(text="CLEAR FILTER").click()
        
        check_box_count = int(d(resourceId="android:id/text1",className="android.widget.CheckedTextView").count)
        print("check box count: "+str(check_box_count))
        selected_check_box = random.randint(0, check_box_count - 1)
        print("selected check box: "+str(selected_check_box))
        selected_check_box = d(resourceId="android:id/text1",className="android.widget.CheckedTextView")[selected_check_box]
        selected_check_box_name = selected_check_box.get_text()
        print("selected check box name: "+str(selected_check_box_name))
        if selected_check_box_name == "-":
            print("not select list or tag, return")
            return
        selected_check_box.click()
        
        d.press("back")
        
        filter_text = d(resourceId="nl.mpcjanssen.simpletask:id/filter_text").get_text()
        print("filter text: "+str(filter_text))
        number = filter_text.split("/")[1][0]
        if number == "0":
            print("no task, return")
            return
        
        assert d(resourceId="nl.mpcjanssen.simpletask:id/tasktext").exists(), "no task"
        
        d(resourceId="nl.mpcjanssen.simpletask:id/tasktext").click()
        
        d(resourceId="nl.mpcjanssen.simpletask:id/update").click()
        
        content = d(resourceId="nl.mpcjanssen.simpletask:id/taskText").get_text()
        print("content: "+str(content))
        assert selected_check_box_name in content, "content doesn't have selected items"
    



t = Test()

setting = Setting(
    apk_path="./apk/simpletask/10.5.2.apk",
    device_serial="emulator-5554",
    output_dir="output/simpletask/1060/random_100/1",
    policy_name="random",
    
    number_of_events_that_restart_app = 100
)
run_android_check_as_test(t,setting)

