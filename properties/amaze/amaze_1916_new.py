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
    def rule_documnets_mainpath(self):
        d(description="Navigate up").click()
        d(resourceId="com.amaze.filemanager:id/design_navigation_view").scroll(steps=10)
        d(text="Documents").click()

    @precondition(lambda self: d(text="Documents").exists()  and not d(text="Settings").exists())
    @rule()
    def rule_documnets(self):
        
        
        assert d(resourceId="com.amaze.filemanager:id/firstline").exists()



t = Test()

setting = Setting(
    apk_path="./apk/amaze/amaze-3.8.4.apk",
    device_serial="emulator-5554",
    output_dir="../output/amaze/1916/1",
    policy_name="random"

)
run_android_check_as_test(t,setting)
