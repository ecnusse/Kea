import sys
sys.path.append("..")
from kea.main import *

class Test(Kea):

    @initialize()
    def set_up(self):
        if d(text="ALLOW").exists():
            d(text="ALLOW").click()

        elif d(text="Allow").exists():
            d(text="Allow").click()

    @main_path()
    def click_sort_should_work_mainpath(self):
        d(description="Navigate up").click()
        d(scrollable = True).scroll.to(text="App Manager")
        d(text="App Manager").click()

    @precondition(lambda self: d(text="App Manager").exists() and d(description="More options").exists())
    @rule()
    def click_sort_should_work(self):
        
        d(resourceId="com.amaze.filemanager:id/sort").click()
        
        assert d(text="Sort By").exists()
    



t = Test()

setting = Setting(
    apk_path="./apk/amaze/amaze-3.8.4.apk",
    device_serial="emulator-5554",
    output_dir="output/amaze/2498/1",
    policy_name="random"

)
run_android_check_as_test(t,setting)

