import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @initialize()
    def set_up(self):
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
    def check_languge_selection(self):
        
        d(text="Language").click()
        
        assert d(scrollable=True).scroll.to(text="Suomi (Finnish)"), "Finnish"
   


t = Test()

setting = Setting(
    apk_path="./apk/omninotes/OmniNotes-5.4.5.apk",
    device_serial="emulator-5554",
    output_dir="output/omninotes/674/mutate/1",
    policy_name="random",

    main_path="main_path/omninotes/674.json"
)
run_android_check_as_test(t,setting)

