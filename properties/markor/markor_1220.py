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
        
        d(text="DONE").click()
        
        
        if d(text="OK").exists():
            d(text="OK").click()
        

        
    
    @precondition(
        lambda self: d(resourceId="net.gsantner.markor:id/action_edit").exists() and
          d(className="android.webkit.WebView").child(className="android.view.View").exists() and not
          d(text="todo").exists()
        )
    @rule()
    def format_should_retain_next_time_open_it(self):
        content = d(className="android.webkit.WebView").child(className="android.view.View").get_text()
        print("content: "+str(content))
        title = d(resourceId="net.gsantner.markor:id/note__activity__text_note_title").get_text()
        print("title: "+str(title))
        d.press("back")
        
        if d(resourceId="net.gsantner.markor:id/action_edit").exists():
            d.press("back")
            
        d(textStartsWith=title).click()
        
        if d(resourceId="net.gsantner.markor:id/action_preview").exists():
            d(resourceId="net.gsantner.markor:id/action_preview").click()
            
        content2 = d(className="android.webkit.WebView").child(className="android.view.View").get_text()
        print("content2: "+str(content2))
        assert content == content2



t = Test()

setting = Setting(
    apk_path="./apk/markor/2.5.0.apk",
    device_serial="emulator-5554",
    output_dir="output/markor/1220/random_100/1",
    policy_name="random",

    main_path="main_path/markor/1220.json"
)
start_kea(t,setting)

