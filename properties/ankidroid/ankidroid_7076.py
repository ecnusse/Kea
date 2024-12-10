import sys
sys.path.append("..")
from kea import *

class Test(KeaTest):
    

    @precondition(
        lambda self: d(text="考研").exists() and d(text="例句").exists() and 
        d(resourceId="com.ichi2.anki:id/action_sync").exists()
    )
    @rule()
    def should_display_name_of_sub_deck(self):
        d(text="考研").click()
        
        assert d(text="例句").exists(), "例句 not found"



if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/ankidroid/2.14alpha1.apk",
        device_serial="emulator-5554",
        output_dir="../output/ankidroid/7076/guided",
        policy_name="guided"
    )
    start_kea(t,setting)
    
