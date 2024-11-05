import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):

    @initialize()
    def set_up(self):
        d(resourceId="it.feio.android.omninotes.alpha:id/next").click()
        
        d(resourceId="it.feio.android.omninotes.alpha:id/next").click()
        
        d(resourceId="it.feio.android.omninotes.alpha:id/next").click()
        
        d(resourceId="it.feio.android.omninotes.alpha:id/next").click()
        
        d(resourceId="it.feio.android.omninotes.alpha:id/next").click()
        
        d(resourceId="it.feio.android.omninotes.alpha:id/done").click()
        
    
    @precondition(lambda self: d(resourceId="it.feio.android.omninotes.alpha:id/search_src_text").exists() and not 
                  d(text="Settings").exists())
    @rule()
    def dataloss_on_search_text(self):
        d.set_orientation('l')
        
        d.set_orientation('n')
        assert d(resourceId="it.feio.android.omninotes.alpha:id/search_src_text").exists() 


t = Test()

setting = Setting(
    apk_path="./apk/omninotes/OmniNotes-6.2.0alpha.apk",
    device_serial="emulator-5554",
    output_dir="output/omninotes/888/random/1",
    policy_name="random",

)
start_kea(t,setting)
