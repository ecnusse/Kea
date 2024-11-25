import sys
sys.path.append("..")
from kea.core import *

class Test(Kea):
    

    @initializer()
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

    @mainPath()
    def change_language_to_chinese_mainpath(self):
        d(description="drawer open").click()
        d(text="Settings").click()
        d(text="Interface").click()


    @precondition(lambda self: d(text="Interface").exists() and d(text="Language").exists())
    @rule()
    def change_language_to_chinese(self):
        
        d(text="Language").click()
        
        d(text="中文 (Chinese Simplified)").click()
        time.sleep(2)
        if d(text="OK").exists():
            d(text="OK").click()
            
        assert d(text="笔记").exists()



if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/omninotes/OmniNotes-6.2.8.apk",
        device_serial="emulator-5554",
        output_dir="../output/omninotes/833/mutate_new",
        policy_name="mutate"
    )
    start_kea(t,setting)
    
