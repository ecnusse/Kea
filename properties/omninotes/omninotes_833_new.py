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
            
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/done").click()
        
        if d(text="OK").exists():
            d(text="OK").click()
            
        
    
    @precondition(lambda self: d(text="Interface").exists() and d(text="Language").exists())
    @rule()
    def change_language_to_chinese(self):
        
        d(text="Language").click()
        
        d(text="中文 (Chinese Simplified)").click()
        time.sleep(2)
        if d(text="OK").exists():
            d(text="OK").click()
            
        assert d(text="笔记").exists()



t = Test()

setting = Setting(
    apk_path="./apk/omninotes/OmniNotes-6.2.8.apk",
    device_serial="emulator-5554",
    output_dir="output/omninotes/833/mutate/1",
    policy_name="random",

    main_path="main_path/omninotes/833.json"
)
run_android_check_as_test(t,setting)

