import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @initialize()
    def set_up(self):
        if not d(text="Setting").exists() and d(description="Open menu").exists():
            d(description="Open menu").click()
            

    @precondition(
        lambda self: d(resourceId="de.danoeh.antennapod.debug:id/discovery_cover").exists() and
          d(resourceId="de.danoeh.antennapod.debug:id/search_src_text").exists() and 
          d(resourceId="de.danoeh.antennapod.debug:id/coverHolder").exists()
    )
    @rule()
    def search_in_one_podcast_should_not_display_others(self):
        assert int(d(resourceId="de.danoeh.antennapod.debug:id/discovery_cover").count) == 1, "discovery cover count not 1"



t = Test()

setting = Setting(
    apk_path="./apk/antennapod/2.0.0.apk",
    device_serial="emulator-5554",
    output_dir="output/antennapod/4488/mutate/1",
    policy_name="random",

    main_path="main_path/antennapod/4488.json"
)
run_android_check_as_test(t,setting)

