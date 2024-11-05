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
        
        d(text="DONE").click()
        
        
        if d(text="OK").exists():
            d(text="OK").click()
        
    
    # bug #1569
    @precondition(lambda self: d(resourceId="net.gsantner.markor:id/toolbar").child(text="QuickNote").exists() and 
                  d(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").exists() and
                  d(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").get_text() is not None and
                  d(description="More options").exists())
    @rule()
    def share_file_to_quicknote_shouldnot_influence_original_content(self):
        original_content = d(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").get_text()
        print("original content: " + str(original_content))
        d(text="Files").click()
        
        d(resourceId="net.gsantner.markor:id/fab_add_new_item").click()
        
        title = st.text(alphabet=string.ascii_lowercase,min_size=1, max_size=6).example()
        print("title: " + title)
        d(resourceId="net.gsantner.markor:id/new_file_dialog__name").set_text(title)
        
        d(text="OK").click()
        
        shared_content = st.text(alphabet=string.printable,min_size=1, max_size=10).example()
        print("shared content: " + shared_content)
        d(className="android.widget.EditText").set_text(shared_content)
        
        d(description="More options").click()
        
        d(text="Share").click()
        
        d(text="Plain Text").click()
        
        d(text="Markor").click()
        
        d(text="QuickNote").click()
        
        d.press("back")
        
        d(text="QuickNote").click()
        
        new_content = d(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").get_text()
        print("new content: " + new_content)
        assert original_content in new_content, "original content should be in new content"
        assert shared_content in new_content, "shared content should be in new content"



t = Test()

setting = Setting(
    apk_path="./apk/markor/2.11.1.apk",
    device_serial="emulator-5554",
    output_dir="output/markor/1569/mutate/1",
    policy_name="random",

    main_path="main_path/markor/1569_new.json"
)
start_kea(t,setting)

