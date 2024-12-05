import sys
sys.path.append("..")
from kea.core import *

class Test(Kea):
    

    @initializer()
    def set_up(self):
        d.press("back")

    @mainPath()
    def text_should_display_when_episodes_is_empty_mainpath(self):
        d(description="Open menu").click()
        d(text="Episodes", reousrceId="de.danoeh.antennapod.debug:id/txtvTitle").click()

    @precondition(
        lambda self: d(text="Episodes").exists() and d(text="NEW").exists() and not d(resourceId="de.danoeh.antennapod:id/status").exists()
    )
    @rule()
    def text_should_display_when_episodes_is_empty(self):
        d(text="NEW").click()
        
        assert d(resourceId="de.danoeh.antennapod:id/emptyViewTitle").exists(), "empty view title not found"



if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/antennapod/885362e5.apk",
        device_serial="emulator-5554",
        output_dir="../output/antennapod/4550/guided",
        policy_name="guided"
    )
    start_kea(t,setting)
    
