import sys
sys.path.append("..")
from kea.core import *

class Test(Kea):
    
    

    @initializer()
    def set_up(self):
        d(text="Get Started").click()

    @mainPath()
    def rotate_device_should_keep_review_card_mainpath(self):
        d(resourceId="com.ichi2.anki:id/deckpicker_name").click()
        d(description="Navigate up").click()
        d(text="Card browser").click()
        d(resourceId="com.ichi2.anki:id/card_sfld").long_click()
        d(description="More options").click()
        d(text="Preview").click()

    @precondition(
        lambda self: d(text="Preview").exists() and
        d(resourceId="com.ichi2.anki:id/preview_next_flashcard").exists() and
        d(resourceId="qa").exists() and
        d(resourceId="qa").get_text() != ""
    )
    @rule()
    def rotate_device_should_keep_review_card(self):
        card_content = d(resourceId="qa").get_text()
        print("card_content: " + str(card_content))
        d.set_orientation("l")
        
        d.set_orientation("n")
        
        new_card_content = d(resourceId="qa").get_text()
        print("new_card_content: " + str(new_card_content))
        assert card_content == new_card_content, "card content should not change"




if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/ankidroid/2.18alpha6.apk",
        device_serial="emulator-5554",
        output_dir="../output/ankidroid/5688/mutate",
        policy_name="mutate",
    
        number_of_events_that_restart_app = 10
    )
    start_kea(t,setting)
    
