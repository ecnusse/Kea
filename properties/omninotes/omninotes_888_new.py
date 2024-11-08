import sys
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @initializer()
    def set_up(self):
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/done").click()


    @mainPath()
    def dataloss_on_search_text_mainpath(self):
        d(resourceId="it.feio.android.omninotes:id/menu_search").click()
        d(resourceId="it.feio.android.omninotes:id/search_plate").set_text("Hello World")
        d.press("enter")
    
    @precondition(lambda self: d(resourceId="it.feio.android.omninotes:id/search_src_text").exists() and not
                  d(text="Settings").exists())
    @rule()
    def dataloss_on_search_text(self):
        d.set_orientation('l')
        
        d.set_orientation('n')
        assert d(resourceId="it.feio.android.omninotes:id/search_src_text").exists()


t = Test()

setting = Setting(
    apk_path="./apk/omninotes/OmniNotes-6.2.8.apk",
    device_serial="emulator-5554",
    output_dir="./output/omninotes/888/mutate_new",
    policy_name="mutate"
)
start_kea(t,setting)

