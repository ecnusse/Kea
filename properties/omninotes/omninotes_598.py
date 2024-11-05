import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @initialize()
    def set_up(self):
        d.set_fastinput_ime(True)
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/done").click()
        
        if d(text="OK").exists():
            d(text="OK").click()
            
        
    
    @precondition(lambda self: d(text="Insert password").exists() and d(text="PASSWORD FORGOTTEN").exists())
    @rule()
    def remove_password_in_setting_should_effect(self):
        
        d(text="OK").click()
        
        if d(text="Insert password").exists():
            print("wrong password")
            return
        d(text="OK").click()
        
        d.press("back")
        
        d.press("back")
        
        d.press("back")
        
        d.press("back")
        
        assert not d(resourceId="it.feio.android.omninotes:id/lockedIcon").exists()
    



t = Test()

setting = Setting(
    apk_path="./apk/omninotes/OmniNotes-5.5.3.apk",
    device_serial="emulator-5554",
    output_dir="output/omninotes/598/random_100/1",
    policy_name="random",
    
    number_of_events_that_restart_app = 100
)
start_kea(t,setting)

