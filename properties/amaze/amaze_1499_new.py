import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    
    @initialize()
    def set_up(self):
        d(description="Navigate up").click()
        
        d(scrollable=True).scroll(steps=10)
        
        d(text="Settings").click()
        
        d(text="Interface").click()
        time.sleep(2)
        d(text="Back navigation").right(className="android.widget.Switch").click()
        
        d.press("back")
        
        d.press("back")


    @precondition(lambda self: d(text="Go Back").exists() and d(resourceId="com.amaze.filemanager:id/second").exists() and d(resourceId="com.amaze.filemanager:id/fullpath").get_text() != "/storage/emulated/0" and not d(resourceId="com.amaze.filemanager:id/donate").exists() and not d(text="Cloud Connection").exists() and not d(resourceId="com.amaze.filemanager:id/check_icon").exists())
    @rule()
    def rule_go_back(self):
        
        original_path = d(resourceId="com.amaze.filemanager:id/fullpath").get_text()
        print("original path: "+str(original_path))
        
        d(text="Go Back",resourceId="com.amaze.filemanager:id/date").click()
        
        after_path = d(resourceId="com.amaze.filemanager:id/fullpath").get_text()
        print("after path: "+str(after_path))
        expected_path = '/'.join(original_path.split("/")[:-1])
        print("expected path: "+str(expected_path))
        assert after_path == expected_path



t = Test()

setting = Setting(
    apk_path="./apk/amaze-3.8.4.apk",
    device_serial="emulator-5554",
    output_dir="output/amaze/1499/1",

    main_path="main_path/amaze/1499.json"
)
run_android_check_as_test(t,setting)

