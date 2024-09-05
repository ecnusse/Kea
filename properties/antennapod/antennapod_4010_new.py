import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @precondition(
        lambda self: d(resourceId="de.danoeh.antennapod:id/butPlay").exists() and 
        d(description="More options").exists() and 
        d(resourceId="de.danoeh.antennapod:id/add_to_favorites_item").exists()
    )
    @rule()
    def click_podcast_should_work(self):
        d(description="More options").click() 
        
        d(text="Open podcast").click()
        
        assert not d(resourceId="de.danoeh.antennapod:id/butFF").exists()





t = Test()

setting = Setting(
    apk_path="./apk/antennapod/3.2.0.apk",
    device_serial="emulator-5554",
    output_dir="output/antennapod/4010/random_100/1",
    policy_name="random",
    
    number_of_events_that_restart_app = 100
)
run_android_check_as_test(t,setting)

