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
        lambda self: d(text="You selected to hide suggestions.").exists()
    )
    @rule()
    def suggestion_should_be_hiden(self):
        assert not d(text="Suggestions by iTunes").exists(), "suggestion found"
        



t = Test()

setting = Setting(
    apk_path="./apk/antennapod/2.1.0-RC2.apk",
    device_serial="emulator-5554",
    output_dir="output/antennapod/4669/mutate/1",
    policy_name="random",

    main_path="main_path/antennapod/4669.json"
)
run_android_check_as_test(t,setting)

