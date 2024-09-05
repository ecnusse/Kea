import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

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



t = Test()

setting = Setting(
    apk_path="./apk/antennapod/3.2.0.apk",
    device_serial="emulator-5554",
    output_dir="output/antennapod/4550/random_100/1",
    policy_name="random",
    
    number_of_events_that_restart_app = 100
)
run_android_check_as_test(t,setting)

