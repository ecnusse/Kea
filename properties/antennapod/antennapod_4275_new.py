import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    
        

    @precondition(
        lambda self: d(resourceId="de.danoeh.antennapod:id/butShowInfo").exists() and 
        d(resourceId="de.danoeh.antennapod:id/ivIsVideo").exists() and
        d(description="Play").exists()
    )
    @rule()
    def play_video_should_not_play_as_audio(self):
        d(description="Play").click()
        
        assert d(resourceId="de.danoeh.antennapod:id/videoPlayerContainer").exists()




t = Test()

setting = Setting(
    apk_path="./apk/antennapod/3.2.0.apk",
    device_serial="emulator-5554",
    output_dir="output/antennapod/4275/random_100/1",
    policy_name="random",
    
    number_of_events_that_restart_app = 100
)
start_kea(t,setting)

