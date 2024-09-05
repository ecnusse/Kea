import string
from kea.main import *
import time
import sys
import re

class Test(Kea):
    

    @initialize()
    def set_up(self):
        d(resourceId="net.gsantner.markor:id/next").click()
        
        d(resourceId="net.gsantner.markor:id/next").click()
        
        d(resourceId="net.gsantner.markor:id/next").click()
        
        d(resourceId="net.gsantner.markor:id/next").click()
        
        d(resourceId="net.gsantner.markor:id/next").click()
        
        d(resourceId="net.gsantner.markor:id/next").click()
        
        d(text="DONE").click()
        
        
        if d(text="OK").exists():
            d(text="OK").click()
        
        
    #bug 552
    @precondition(
        lambda self: d(resourceId="net.gsantner.markor:id/fab_add_new_item").exists() and 
        d(resourceId="net.gsantner.markor:id/ui__filesystem_item__title").exists() and
        d(resourceId="net.gsantner.markor:id/ui__filesystem_item__title").count >= 2 and
        d(text="markor").exists() and not 
        d(text="Settings").exists() and not 
        d(text="Date").exists() and not 
        d(resourceId="net.gsantner.markor:id/action_rename_selected_item").exists()
        )
    @rule()
    def modify_content_should_update_time(self):
        file_count = d(resourceId="net.gsantner.markor:id/ui__filesystem_item__title").count
        print("file count: "+str(file_count))
        if file_count == 0:
            print("no file ")
            return
        file_index = random.randint(0, file_count - 1)
        selected_file = d(resourceId="net.gsantner.markor:id/ui__filesystem_item__title")[file_index]
        file_name = selected_file.info['text']
        
        if "." not in file_name or ".." in file_name:
            print("not a file")
            return
        print("file name: "+str(file_name))
        selected_file.click()
        
        new_content = st.text(alphabet=string.ascii_lowercase,min_size=6, max_size=10).example()
        print("new content: "+str(new_content))
        d(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").set_text(new_content)
        
        d(description="Navigate up").click()
        
        
        hour_minite = str(d(resourceId="com.android.systemui:id/clock").get_text())
        print("hour minite: "+str(hour_minite))
        file_time = d(text=file_name).sibling(resourceId="net.gsantner.markor:id/ui__filesystem_item__description").info['text']
        print("file time: "+str(file_time))
        file_hour_minite = str(file_time.split(" ")[1])
        print("file hour minite: "+str(file_hour_minite))
        assert file_hour_minite == hour_minite



t = Test()

setting = Setting(
    apk_path="./apk/markor/1.7.6.apk",
    device_serial="emulator-5554",
    output_dir="output/markor/552/mutate/1",
    policy_name="random",

    main_path="main_path/markor/552.json"
)
run_android_check_as_test(t,setting)

