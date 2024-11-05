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
        
    @precondition(
        lambda self: d(resourceId="net.gsantner.markor:id/fab_add_new_item").exists() and 
        d(resourceId="net.gsantner.markor:id/opoc_filesystem_item__title").exists() and 
        int(d(resourceId="net.gsantner.markor:id/opoc_filesystem_item__title").count) > 2 and 
        d(resourceId="net.gsantner.markor:id/nav_notebook").info["selected"] and 
        d(resourceId="net.gsantner.markor:id/action_go_to").exists()
    )
    @rule()
    def view_file_should_exist_in_recent_viewed_documents(self):
        file_count = d(resourceId="net.gsantner.markor:id/opoc_filesystem_item__title").count
        print("file count: "+str(file_count))
        if file_count == 0:
            print("no file to rename")
            return
        file_index = random.randint(0, file_count - 1)
        selected_file = d(resourceId="net.gsantner.markor:id/opoc_filesystem_item__title")[file_index]
        file_name = selected_file.info['text']
        if "." not in file_name or ".." in file_name:
            print("not a file")
            return
        print("file name: "+str(file_name))
        selected_file.click()
        
        d.press("back")
        
        if not d(resourceId="net.gsantner.markor:id/action_go_to").exists():
            d.press("back")
            
        d(resourceId="net.gsantner.markor:id/action_go_to").click()
        
        d(text="Recently viewed documents").click()
        
        assert d(text=file_name).exists(), "file not in recently viewed documents"





t = Test()

setting = Setting(
    apk_path="./apk/markor/2.11.1.apk",
    device_serial="emulator-5554",
    output_dir="output/markor/1478/mutate/1",
    policy_name="random",

    main_path="main_path/markor/1478_new.json"
)
start_kea(t,setting)

