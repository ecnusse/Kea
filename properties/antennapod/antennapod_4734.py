import sys
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @initialize()
    def set_up(self):
        d.press("back")

    @main_path()
    def share_menu_should_display_mainpath(self):
        d(description="Open menu").click()
        d(text="Add Podcast", resourceId="de.danoeh.antennapod.debug:id/txtvTitle").click()
        d(resourceId="de.danoeh.antennapod.debug:id/discovery_cover").click()
        d(text="Subscribe").click()

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
    output_dir="../output/antennapod/4734/mutate",
    policy_name="mutate"
)
start_kea(t,setting)

