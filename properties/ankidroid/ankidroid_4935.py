import sys
sys.path.append("..")
from kea.main import *

class Test(Kea):
    
    @main_path()
    def back_should_navigate_to_last_page_mainpath(self):
        d(description="Navigate up").click()
        d(text="Settings").click()
        d(text="Appearance").click()

    @precondition(
        lambda self: d(text="Day theme").exists() and
        d(text="Appearance").exists()
        )
    @rule()
    def back_should_navigate_to_last_page(self):
        d.press("back")
        
        assert d(text="Preferences").exists()
        


t = Test()

setting = Setting(
    apk_path="./apk/ankidroid/2.9alpha29.apk",
    device_serial="emulator-5554",
    output_dir="../output/ankidroid/4935/mutate",
    policy_name="mutate"
)
start_kea(t,setting)

