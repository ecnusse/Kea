import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @precondition(
        lambda self: d(resourceId="de.danoeh.antennapod:id/butShowInfo").exists()
    )
    @rule()
    def share_menu_should_display(self):
        d(resourceId="de.danoeh.antennapod:id/butShowInfo").click()
        
        assert d(resourceId="de.danoeh.antennapod:id/share_item").exists(), "share not found"


t = Test()

setting = Setting(
    apk_path="./apk/antennapod/3.2.0.apk",
    device_serial="emulator-5554",
    output_dir="output/antennapod/4734/mutate_new/1",
    policy_name="random",

    main_path="main_path/antennapod/5003_new.json"
)
run_android_check_as_test(t,setting)

