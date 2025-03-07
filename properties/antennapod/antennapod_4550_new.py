import sys
sys.path.append("..")
from kea import *

class Test(KeaTest):

    @mainPath()
    def text_should_display_when_episodes_is_empty_mainpath(self):
        d(description="Open menu").click()
        d(text="Episodes").click()

    @precondition(
        lambda self: d(resourceId="de.danoeh.antennapod:id/toolbar").exists() and 
        d(resourceId="de.danoeh.antennapod:id/toolbar").child(text="Episodes",className="android.widget.TextView").exists() and 
        d(resourceId="de.danoeh.antennapod:id/action_favorites").exists() and not 
        d(resourceId="de.danoeh.antennapod:id/container").exists() and not 
        d(text="Settings").exists()
    )
    @rule()
    def text_should_display_when_episodes_is_empty(self):

        assert d(resourceId="de.danoeh.antennapod:id/emptyViewTitle").exists(), "empty view title not found"



if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/antennapod/3.2.0.apk",
        device_serial="emulator-5554",
        output_dir="../output/antennapod/4550/guided_new",
        policy_name="guided",
        
        number_of_events_that_restart_app = 100
    )
    start_kea(t,setting)
    
