import string
from kea.main import *
import time
import sys
import re

class Test(Kea):
    
    @initialize()
    def set_up(self):    
        
        if d(text="OK").exists():
            d(text="OK").click()
    
    # bug #389
    @precondition(lambda self: d(resourceId="net.gsantner.markor:id/fab_add_new_item").exists() and 
                  d(resourceId="net.gsantner.markor:id/note_title").count < 4)
    @rule()
    def create_file_should_only_create_one(self):
        file_count = int(d(resourceId="net.gsantner.markor:id/note_title").count)
        print("file_count: " + str(file_count))
        d(resourceId="net.gsantner.markor:id/fab_add_new_item").click()
        
        content = st.text(alphabet=string.ascii_lowercase,min_size=5, max_size=6).example()
        print("content: " + str(content))
        d(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").set_text(content)
        
        d.press("back")
        if d(resourceId="net.gsantner.markor:id/action_preview").exists():
            d.press("back")
        
        new_count = int(d(resourceId="net.gsantner.markor:id/note_title").count)
        print("new_count: " + str(new_count))
        assert new_count == file_count + 1
        


t = Test()

setting = Setting(
    apk_path="./apk/markor/1.3.0.apk",
    device_serial="emulator-5554",
    output_dir="output/markor/389/mutate/1",
    policy_name="random",

    main_path="main_path/markor/389.json"
)
run_android_check_as_test(t,setting)

