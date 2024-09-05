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
        
        
    #bug 1220
    @precondition(
        lambda self: d(resourceId="net.gsantner.markor:id/fab_add_new_item").exists() and not d(text="Settings").exists() and not d(text="Date").exists() and not d(resourceId="net.gsantner.markor:id/action_rename_selected_item").exists()
        )
    @rule()
    def change_file_format_should_work(self):
        file_count = d(resourceId="net.gsantner.markor:id/opoc_filesystem_item__title").count
        print("file count: "+str(file_count))
        if file_count == 0:
            print("no file ")
            return
        file_index = random.randint(0, file_count - 1)
        selected_file = d(resourceId="net.gsantner.markor:id/opoc_filesystem_item__title")[file_index]
        file_name = selected_file.info['text']
        
        if "." not in file_name or ".." in file_name:
            print("not a file")
            return
        print("file name: "+str(file_name))
        selected_file.click()
        
        d(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").set_text("# test")
        
        d(description="More options").click()
        
        d(text="File settings").click()
        
        d(text="Format").click()
        
        d(text="Markdown").click()
        
        d(resourceId="net.gsantner.markor:id/action_preview").click()
        
        assert "#" not in d(className="android.webkit.WebView").child(className="android.view.View").info["contentDescription"], "1 markdown format failed"
        
        d.press("back")
        
        d.press("back")
        
        d(resourceId="net.gsantner.markor:id/opoc_filesystem_item__title")[file_index].click()
        
        assert "#" not in d(className="android.webkit.WebView").child(className="android.view.View").info["contentDescription"], "2 markdown format failed"
    





t = Test()

setting = Setting(
    apk_path="./apk/markor/2.11.1.apk",
    device_serial="emulator-5554",
    output_dir="output/markor/1220/1",
    explore_event_count=500,
    diverse_event_count=500,
    policy_name="random",
)

