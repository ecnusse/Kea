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
        lambda self: d(text="Episodes").exists() and d(text="NEW").exists() and not d(resourceId="de.danoeh.antennapod:id/status").exists()
    )
    @rule()
    def text_should_display_when_episodes_is_empty(self):
        d(text="NEW").click()
        
        assert d(resourceId="de.danoeh.antennapod:id/emptyViewTitle").exists(), "empty view title not found"



t = Test()

setting = Setting(
    apk_path="./apk/antennapod/885362e5.apk",
    device_serial="emulator-5554",
    output_dir="output/antennapod/4550/mutate/1",
    policy_name="random",

    main_path="main_path/antennapod/4550.json"
)
start_kea(t,setting)

