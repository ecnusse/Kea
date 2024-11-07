import sys
sys.path.append("..")
from kea.main import *

class Test(Kea):

    @main_path()
    def rotate_device_should_keep_review_card_mainpath(self):
        d(resourceId="com.ichi2.anki:id/deckpicker_name").click()
        d(description="Navigate up").click()
        d(text="Card browser").click()
        d(resourceId="com.ichi2.anki:id/card_sfld").long_click()
        d(description="More options").click()
        d(text="Preview").click()

    @precondition(
        lambda self: d(text="Preview").exists() and
        d(resourceId="com.ichi2.anki:id/nextTime2").exists() and 
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




t = Test()

setting = Setting(
    apk_path="./apk/ankidroid/2.9.2.apk",
    device_serial="emulator-5554",
    output_dir="../output/ankidroid/5688/mutate",
    policy_name="mutate"
)
start_kea(t,setting)

