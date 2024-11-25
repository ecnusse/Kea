import sys
sys.path.append("..")
from kea.core import *

class Test(Kea):
    

    @initializer()
    def set_up(self):
        pass

    @mainPath()
    def show_answer_button_should_only_display_one_mainpath(self):
        d(resourceId="com.ichi2.anki:id/deckpicker_name").click()
        d(description="Navigate up").click()
        d(text="Card browser").click()
        d(resourceId="com.ichi2.anki:id/card_sfld").long_click()
        d(description="More options").click()
        d(text="Preview").click()

    @precondition(
        lambda self: d(text="Preview").exists() and d(text="SHOW ANSWER").exists()
    )
    @rule()
    def show_answer_button_should_only_display_one(self):
        assert d(text="SHOW ANSWER").count == 1, "SHOW ANSWER button should only display one"
        


if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/ankidroid/2.13alpha26.apk",
        device_serial="emulator-5554",
        output_dir="../output/ankidroid/7027/mutate",
        policy_name="mutate",
        
        number_of_events_that_restart_app = 100
    )
    start_kea(t,setting)
    
