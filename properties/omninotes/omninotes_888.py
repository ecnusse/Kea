import sys
sys.path.append("..")
from kea import *

class Test(KeaTest):

    @initializer()
    def set_up(self):
        d(resourceId="it.feio.android.omninotes.alpha:id/next").click()
        
        d(resourceId="it.feio.android.omninotes.alpha:id/next").click()
        
        d(resourceId="it.feio.android.omninotes.alpha:id/next").click()
        
        d(resourceId="it.feio.android.omninotes.alpha:id/next").click()
        
        d(resourceId="it.feio.android.omninotes.alpha:id/next").click()
        
        d(resourceId="it.feio.android.omninotes.alpha:id/done").click()

    @mainPath()
    def dataloss_on_search_text_mainpath(self):
        d(resourceId="it.feio.android.omninotes.alpha:id/menu_search").click()
        d(resourceId="it.feio.android.omninotes.alpha:id/search_src_text").set_text("Hello World")
        d.press("enter")
    
    @precondition(lambda self: d(resourceId="it.feio.android.omninotes.alpha:id/search_src_text").exists() and not 
                  d(text="Settings").exists())
    @rule()
    def dataloss_on_search_text(self):
        d.set_orientation('l')
        
        d.set_orientation('n')
        assert d(resourceId="it.feio.android.omninotes.alpha:id/search_src_text").exists() 


if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/omninotes/OmniNotes-6.2.0alpha.apk",
        device_serial="emulator-5554",
        output_dir="../output/omninotes/888/guided",
        policy_name="guided"
    )
    start_kea(t,setting)
