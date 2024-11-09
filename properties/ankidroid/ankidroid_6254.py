import sys
sys.path.append("..")
from kea.main import *

class Test(Kea):
     
    @initializer()
    def set_up(self):
        if d(text="OK").exists():
            d(text="OK").click()

    @mainPath()
    def yue_should_display_in_language_mainpath(self):
        d(description="Navigate up").click()
        d(text="Settings").click()
        d(text="AnkiDroid").click()

    @precondition(
        lambda self: d(text="Language").exists() and 
        d(text="AnkiDroid").exists() 
    )
    @rule()
    def yue_should_display_in_language(self):
        d(text="Language").click()
        
        assert d(scrollable=True).scroll.to(text="yue")



t = Test()

setting = Setting(
    apk_path="./apk/ankidroid/2.11alpha6.apk",
    device_serial="emulator-5554",
    output_dir="../output/ankidroid/6254/mutate",
    policy_name="mutate"
)
start_kea(t,setting)

