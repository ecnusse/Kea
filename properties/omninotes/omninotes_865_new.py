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
        
        
        
    @precondition(lambda self: d(resourceId="it.feio.android.omninotes:id/menu_attachment").exists())
    @rule()
    def sroll_down_on_attachment(self):
        
        d(resourceId="it.feio.android.omninotes:id/menu_attachment").click()
        
        if d(text="Pushbullet").exists():
            return True
        if d(scrollable=True).exists():
            d(scrollable=True).scroll(steps=10)
        
        assert d(text="Pushbullet").exists()
    


t = Test()

setting = Setting(
    apk_path="./apk/omninotes/OmniNotes-6.1.0.apk",
    device_serial="emulator-5554",
    output_dir="output/omninotes/865/mutate/1",
    policy_name="random",

    main_path="main_path/omninotes/865.json"
)
run_android_check_as_test(t,setting)

