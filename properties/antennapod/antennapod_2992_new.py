import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @precondition(
        lambda self: d(resourceId="de.danoeh.antennapod:id/imgvCover").exists() and d(resourceId="de.danoeh.antennapod:id/audio_controls").exists()
    )
    @rule()
    def rotate_device_shouldnot_make_cover_disappear(self):
        d.set_orientation('l')
        
        d.set_orientation('n')
        
        assert d(resourceId="de.danoeh.antennapod:id/imgvCover").exists()





t = Test()

setting = Setting(
    apk_path="./apk/antennapod/3.2.0.apk",
    device_serial="emulator-5554",
    output_dir="output/antennapod/2992/mutate_new/1",
    policy_name="random",
    timeout=86400,
    number_of_events_that_restart_app = 100,
    main_path="main_path/antennapod/2992_new.json"
)
run_android_check_as_test(t,setting)

