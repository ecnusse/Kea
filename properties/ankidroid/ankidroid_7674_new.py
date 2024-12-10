import sys
sys.path.append("..")
from kea import *

class Test(KeaTest):

    @mainPath()
    def reposition_should_not_be_missing_mainpath(self):
        d(description="Open drawer").click()
        d(text="Card browser").click()
        d(resourceId="com.ichi2.anki:id/dropdown_deck_name").click()
        d(text="All decks").click()

    @precondition(
        lambda self: 
        d(resourceId="com.ichi2.anki:id/card_sfld").exists() and
        d(resourceId="com.ichi2.anki:id/dropdown_deck_name").exists() 
    )
    @rule()
    def reposition_should_not_be_missing(self):
        random_select_card = random.choice(d(resourceId="com.ichi2.anki:id/card_sfld"))
        random_select_card.long_click()
        
        d(description="More options").click()
        
        d(text="Reposition").click()
        
        d(resourceId="com.ichi2.anki:id/dialog_text_input").set_text("1")
        
        d(resourceId="android:id/button1").click()
        
        # go to "more" and check
        d(description="More options").click()
        
        assert d(text="Undo reposition").exists(), "missing Undo reposition"




if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/ankidroid/2.13.5.apk",
        device_serial="emulator-5554",
        output_dir="../output/ankidroid/7674/guided",
        policy_name="guided"
    )
    start_kea(t,setting)
    
