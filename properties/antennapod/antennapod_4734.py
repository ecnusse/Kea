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
        lambda self: d(resourceId="de.danoeh.antennapod.debug:id/butShowInfo").exists()
    )
    @rule()
    def share_menu_should_display(self):
        d(resourceId="de.danoeh.antennapod.debug:id/butShowInfo").click()
        
        d(description="More options").click()
        
        assert d(text="Share").exists(), "share not found"


t = Test()

setting = Setting(
    apk_path="./apk/antennapod/2.1.0.apk",
    device_serial="emulator-5554",
    output_dir="output/antennapod/4734/mutate/1",
    policy_name="random",

    main_path="main_path/antennapod/4734.json"
)
run_android_check_as_test(t,setting)

