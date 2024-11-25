import sys
sys.path.append("..")
from kea.core import *

class Test(Kea):
    

    @precondition(
        lambda self: 
        d(resourceId="com.ichi2.anki:id/fab_main").exists() and
        d(description="More options").exists() and not 
        d(text="Card browser").exists()
    )
    @rule()
    def right_swipe_from_the_center_should_not_open_the_menu(self):
        print("precondition satisfied, executing.")
        # right swipe
        d.drag(0.5, 0.5, 0.9, 0.5)
        
        assert not d(resourceId="com.ichi2.anki:id/design_menu_item_text").exists(), "mistakenly open the menu"




if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/ankidroid/2.18alpha6.apk",
        device_serial="emulator-5554",
        output_dir="output/ankidroid/8235/mutate/1",
        policy_name="random"
    )
    start_kea(t,setting)
    
