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
        
        
    
    # bug #1961
    @precondition(lambda self: d(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").exists() and 
                  d(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").get_text() is not None and 
                  d(resourceId="net.gsantner.markor:id/action_search").exists())
    @rule()
    def search_in_the_file(self):
        content = d(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").info['text']
        
        words = content.split()
        search_word = random.choice(words)
        print("search word: "+str(search_word))
        d(resourceId="net.gsantner.markor:id/action_search").click()
        
        d(text="Search").set_text(search_word)
        
        search_result = d(resourceId="android:id/text1")
        search_result_count = search_result.count
        print("search result count: "+str(search_result_count))
        assert search_result_count > 0
        search_result_text = search_result.info['text']
        print("search result text: "+str(search_result_text))
        assert search_word in str(search_result_text)




t = Test()

setting = Setting(
    apk_path="./apk/markor/2.11.1.apk",
    device_serial="emulator-5554",
    output_dir="output/markor/1961/1",
    policy_name="random",

    main_path="main_path/markor/1961_new.json"
)
run_android_check_as_test(t,setting)

