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
    def sroll_down_on_attachment_mainpath(self):
        d(resourceId="it.feio.android.omninotes:id/fab_expand_menu_button").long_click()
        
    @precondition(lambda self: d(resourceId="it.feio.android.omninotes:id/menu_attachment").exists())
    @rule()
    def sroll_down_on_attachment(self):
        
        d(resourceId="it.feio.android.omninotes:id/menu_attachment").click()
        
        if d(text="Pushbullet").exists():
            return True
        if d(scrollable=True).exists():
            d(scrollable=True).scroll(steps=10)
        
        assert d(text="Pushbullet").exists()
    


if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/omninotes/OmniNotes-6.1.0.apk",
        device_serial="emulator-5554",
        output_dir="../output/omninotes/865/mutate_new",
        policy_name="mutate"
    )
    start_kea(t,setting)
    
