import sys
sys.path.append("..")
from kea.core import *

class Test(Kea):
    

    @initializer()
    def set_up(self):
        d.press("back")

    @mainPath()
    def suggestion_should_be_hiden_mainpath(self):
        d(description="Open menu").click()
        d(text="Add Podcast", resourceId="de.danoeh.antennapod.debug:id/txtvTitle").click()
        d(resourceId="de.danoeh.antennapod.debug:id/discover_more").click()
        d(resourceId="de.danoeh.antennapod.debug:id/spinner_country").click()
        d(scrollable=True).scroll.to(text="Hide")
        d(text="Hide").click()
        d.press("back")

    @precondition(
        lambda self: d(text="You selected to hide suggestions.").exists()
    )
    @rule()
    def suggestion_should_be_hiden(self):
        assert not d(text="Suggestions by iTunes").exists(), "suggestion found"
        



if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/antennapod/2.1.0-RC2.apk",
        device_serial="emulator-5554",
        output_dir="../output/antennapod/4669/mutate",
        policy_name="mutate"
    )
    start_kea(t,setting)
    
