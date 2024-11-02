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
    def should_not_contains_fba_mainpath(self):
        d(description = "Navigate up").click()
        d(scrollable=True).scroll.to(text="FTP Server")
        d(text="FTP Server").click()

    @precondition(lambda self: d(resourceId="com.amaze.filemanager:id/ftpserver_fragment").exists() and not d(text="Settings").exists())
    @rule()
    def should_not_contains_fba(self):
        assert not d(resourceId="com.amaze.filemanager:id/sd_main_fab").exists()



t = Test()

setting = Setting(
    apk_path="./apk/amaze/amaze-3.4.3.apk",
    device_serial="emulator-5554",
    output_dir="output/amaze/1933/random_100/1",
    policy_name="random"
)
run_android_check_as_test(t,setting)

