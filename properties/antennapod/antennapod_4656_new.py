import sys
sys.path.append("..")
from kea.main import *

class Test(Kea):
    



    @main_path()
    def clear_download_log_should_work_main_path(self):
        d(description="Open menu").click()
        d(text="Add podcast").click()
        d(text="Show suggestions").click()
        d(resourceId="de.danoeh.antennapod:id/discovery_cover").click()
        d(text="Subscribe").click()
        d(resourceId="de.danoeh.antennapod:id/secondaryActionButton").click()
        d(description="Open menu").click()
        d(text="Downloads").click()
        d(resourceId="de.danoeh.antennapod:id/action_download_logs").click()

    @precondition(
        lambda self: d(text="Download log").exists() and
        d(resourceId="de.danoeh.antennapod:id/clear_logs_item").exists() and
        d(resourceId="de.danoeh.antennapod:id/list").exists()
    )
    @rule()
    def clear_download_log_should_work(self):
        d(resourceId="de.danoeh.antennapod:id/clear_logs_item").click()
        
        assert not d(resourceId="de.danoeh.antennapod:id/list").exists(), "clear log failed"



t = Test()

setting = Setting(
    apk_path="./apk/antennapod/3.2.0.apk",
    device_serial="emulator-5554",
    output_dir="../output/antennapod/4656/mutate_new",
    policy_name="mutate"
)
run_android_check_as_test(t,setting)

