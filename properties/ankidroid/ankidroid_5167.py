import sys
sys.path.append("..")
from kea.main import *

class Test(Kea):
    
    @mainPath()
    def reschedule_should_display_another_card_mainpath(self):
        d(resourceId="com.ichi2.anki:id/deckpicker_name").click()

    @precondition(
        lambda self: d(resourceId="com.ichi2.anki:id/flashcard_frame").exists() and
        d(resourceId="com.ichi2.anki:id/action_mark_card").exists() and
        d(resourceId="com.ichi2.anki:id/bottom_area_layout").exists()
    )
    @rule()
    def reschedule_should_display_another_card(self):
        content = d(resourceId="content").child(className="android.view.View").get_text()
        print("content: " + str(content))
        d(description="More options").click()
        
        d(text="Scheduling").click()
        
        d(text="Reschedule").click()
        
        d(className="android.widget.EditText").set_text("1")
        
        d(text="OK").click()
        
        new_content = d(resourceId="content").child(className="android.view.View").get_text()
        print("new_content: " + str(new_content))
        assert content != new_content, "should display another card"




if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/ankidroid/2.9alpha55.apk",
        device_serial="emulator-5554",
        output_dir="output/ankidroid/5167/mutate/1",
        policy_name="random"
    )
    start_kea(t,setting)
    
