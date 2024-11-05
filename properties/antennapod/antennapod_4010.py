import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @initialize()
    def set_up(self):
        d.press("back")

    @precondition(
        lambda self: d(resourceId="de.danoeh.antennapod.debug:id/butPlay").exists() and 
        d(description="More options").exists() and 
        d(resourceId="de.danoeh.antennapod.debug:id/add_to_favorites_item").exists()
    )
    @rule()
    def click_podcast_should_work(self):
        d(description="More options").click() 
        
        d(text="Open Podcast").click()
        
        assert not d(resourceId="de.danoeh.antennapod.debug:id/butFF").exists()



t = Test()

setting = Setting(
    apk_path="./apk/antennapod/2.0.0-alpha1.apk",
    device_serial="emulator-5554",
    output_dir="output/antennapod/4010/mutate/1",
    policy_name="random",

    main_path="main_path/antennapod/4010.json"
)
start_kea(t,setting)

