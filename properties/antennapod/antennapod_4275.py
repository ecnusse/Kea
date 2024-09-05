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
        lambda self: d(resourceId="de.danoeh.antennapod:id/butShowInfo").exists() and not 
        d(resourceId="de.danoeh.antennapod:id/imgvType").exists() and
        d(description="Play").exists()
    )
    @rule()
    def play_video_should_not_play_as_audio(self):
        d(description="Play").click()
        
        assert not d(resourceId="de.danoeh.antennapod:id/playerFragment").exists()




t = Test()

setting = Setting(
    apk_path="./apk/antennapod/1.8.1.apk",
    device_serial="emulator-5554",
    output_dir="output/antennapod/4275/mutate/1",
    policy_name="random",

    main_path="main_path/antennapod/4275.json"
)
run_android_check_as_test(t,setting)

