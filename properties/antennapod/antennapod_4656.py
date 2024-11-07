import sys
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @initialize()
    def set_up(self):
        d.press("back")

    @main_path()
    def clear_download_log_should_work_main_path(self):
        d(description="Open menu").click()
        d(text="Add Podcast", resourceId="de.danoeh.antennapod.debug:id/txtvTitle").click()
        d(resourceId="de.danoeh.antennapod.debug:id/discovery_cover").click()
        d(text="Subscribe").click()
        d(resourceId="de.danoeh.antennapod.debug:id/secondaryActionButton").click()
        d(description="Open menu").click()
        d(text="Downloads", resourceId="de.danoeh.antennapod.debug:id/txtvTitle").click()
        d(text="LOG").click()

    @precondition(
        lambda self: d(text="Downloads").exists() and 
        d(resourceId="de.danoeh.antennapod.debug:id/clear_logs_item").exists() and
        d(resourceId="de.danoeh.antennapod.debug:id/container").exists()
    )
    @rule()
    def clear_download_log_should_work(self):
        d(resourceId="de.danoeh.antennapod.debug:id/clear_logs_item").click()
        
        assert not d(resourceId="de.danoeh.antennapod.debug:id/container").exists(), "clear log failed"



t = Test()

setting = Setting(
    apk_path="./apk/antennapod/2.1.0-RC1.apk",
    device_serial="emulator-5554",
    output_dir="../output/antennapod/4656/mutate",
    policy_name="mutate"
)
start_kea(t,setting)

