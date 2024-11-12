import sys
sys.path.append("..")
from kea.main import *

class Test(Kea):

    @mainPath()
    def share_menu_should_display_mainpath(self):
        d(description="Open menu").click()
        d(text="Add podcast").click()
        d(text="Show suggestions").click()
        d(resourceId="de.danoeh.antennapod:id/discovery_cover").click()
        d(text="Subscribe").click()

    @precondition(
        lambda self: d(resourceId="de.danoeh.antennapod:id/butShowInfo").exists()
    )
    @rule()
    def share_menu_should_display(self):
        d(resourceId="de.danoeh.antennapod:id/butShowInfo").click()
        
        assert d(resourceId="de.danoeh.antennapod:id/share_item").exists(), "share not found"


if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/antennapod/3.2.0.apk",
        device_serial="emulator-5554",
        output_dir="../output/antennapod/4734/mutate_new",
        policy_name="mutate"
    )
    start_kea(t,setting)
    
