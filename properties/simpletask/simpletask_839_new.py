import sys
from socket import send_fds

sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @initialize()
    def set_up(self):
        if d(text="OK").exists():
            d(text="OK").click()

    @main_path()
    def unclick_filter_should_work_mainpath(self):
        d(resourceId="nl.mpcjanssen.simpletask:id/fab").click()
        d(resourceId="nl.mpcjanssen.simpletask:id/btnProject").click()
        d(resourceId="nl.mpcjanssen.simpletask:id/custom").click()
        d.send_keys("Hello world")
        d(text="OK").click()
        d(resourceId="nl.mpcjanssen.simpletask:id/btnSave").click()

    @precondition(
        lambda self: int(d(resourceId="nl.mpcjanssen.simpletask:id/tasktext").count) > 0 and not d(resourceId="nl.mpcjanssen.simpletask:id/filter_text").exists() and not d(text="Quick filter").exists() and not d(text="Settings").exists() and not d(text="Saved filters").exists()
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
    apk_path="./apk/simpletask/11.0.1.apk",
    device_serial="emulator-5554",
    output_dir="../output/simpletask/mutate_new",
    policy_name="mutate",

)
run_android_check_as_test(t,setting)

