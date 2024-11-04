import sys
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @initialize()
    def set_up(self):
        if d(text="OK").exists():
            d(text="OK").click()

    @main_path()
    def click_share_should_work_mainpath(self):
        d(description="More options").click()

    @precondition(
        lambda self: d(text="Share").exists() and d(text="Settings").exists()
    )
    @rule()
    def click_share_should_work(self):
        d(text="Share").click()
        
        assert d(text="Drive").exists()
        


t = Test()

setting = Setting(
    apk_path="./apk/simpletask/8.2.0.apk",
    device_serial="emulator-5554",
    output_dir="../output/simpletask/538/mutate",
    policy_name="mutate"
)
run_android_check_as_test(t,setting)

