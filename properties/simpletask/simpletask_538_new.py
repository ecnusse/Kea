import sys
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @initializer()
    def set_up(self):
        if d(text="OK").exists():
            d(text="OK").click()

    @mainPath()
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
    apk_path="./apk/simpletask/11.0.1.apk",
    device_serial="emulator-5554",
    output_dir="../output/simpletask/538/mutate_new",
    policy_name="mutate"
)
start_kea(t,setting)

