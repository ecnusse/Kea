import sys
sys.path.append("..")
from kea.main import *

class Test(Kea):
    
    @mainPath()
    def only_new_card_can_be_reposition_mainpath(self):
        d(text="考研").click()
        d.press("back")
        d(description="Navigate up").click()
        d(text="Card browser").click()

    @precondition(
        lambda self: d(resourceId="com.ichi2.anki:id/card_sfld").exists() and
        d(resourceId="com.ichi2.anki:id/action_search").exists()
    )
    @rule()
    def only_new_card_can_be_reposition(self):
        d(resourceId="com.ichi2.anki:id/action_search").click()
        
        d(resourceId="com.ichi2.anki:id/search_src_text").set_text("is:learn")
        
        d.set_fastinput_ime(False) #
        d.send_action("search") # 
        
        if not d(resourceId="com.ichi2.anki:id/card_sfld").exists():
            print("no learned card found")
            return
        d(resourceId="com.ichi2.anki:id/card_sfld").long_click()
        
        d(description="More options").click()
        
        d(text="Reposition").click()
        
        assert not d(text="Reposition new card").exists(), "Reposition new card found"
        





if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/ankidroid/2.9alpha58.apk",
        device_serial="emulator-5554",
        output_dir="../output/ankidroid/5216/mutate",
        policy_name="mutate"
    )
    start_kea(t,setting)
    
