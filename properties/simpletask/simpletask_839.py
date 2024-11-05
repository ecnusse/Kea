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
        lambda self: int(d(resourceId="nl.mpcjanssen.simpletask:id/tasktext").count) > 0 and not 
        d(resourceId="nl.mpcjanssen.simpletask:id/filter_text").exists() and not 
        d(text="Quick filter").exists() and not 
        d(text="Settings").exists() and not 
        d(text="Saved filters").exists()
    )
    @rule()
    def unclick_filter_should_work(self):
        d(resourceId="nl.mpcjanssen.simpletask:id/filter").click()
        
        filter_count = int(d(resourceId="android:id/text1").count)
        print("filter count: "+str(filter_count))
        selected_filter_index = random.randint(0, filter_count - 1)
        print("selected filter: "+str(selected_filter_index))
        d(resourceId="android:id/text1")[selected_filter_index].click()
        
        d(resourceId="nl.mpcjanssen.simpletask:id/menu_filter_action").click()
        
        assert d(resourceId="nl.mpcjanssen.simpletask:id/filter_text").exists(), "filter text should exist"
        

        d(resourceId="nl.mpcjanssen.simpletask:id/filter").click()
        
        d(resourceId="android:id/text1")[selected_filter_index].click()
        
        d(resourceId="nl.mpcjanssen.simpletask:id/menu_filter_action").click()
        
        assert not d(resourceId="nl.mpcjanssen.simpletask:id/filter_text").exists(), "filter text should not exist"

        


t = Test()

setting = Setting(
    apk_path="./apk/simpletask/10.0.7.apk",
    device_serial="emulator-5554",
    output_dir="output/simpletask/839/mutate/1",
    policy_name="random",

    main_path="main_path/simpletask/839.json"
)
start_kea(t,setting)

