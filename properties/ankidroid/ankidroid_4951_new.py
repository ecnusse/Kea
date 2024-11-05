import sys
sys.path.append("..")
from kea.main import *

class Test(Kea):

    @initialize()
    def set_up(self):
        d(text="Get Started").click()

    @main_path()
    def rule_allow_permission_three_points_exists_mainpath(self):
        d(text="ALLOW").click()

    @precondition(
        lambda self: d(text="AnkiDroid").exists() and
        d(resourceId="com.ichi2.anki:id/fab_main").exists() and
        d(resourceId="com.ichi2.anki:id/deckpicker_name").exists()
    )
    @rule()
    def rule_allow_permission_three_points_exists(self):
        
        assert d(description="More options").exists()
        



t = Test()

setting = Setting(
    apk_path="./apk/ankidroid/2.18alpha6.apk",
    device_serial="emulator-5554",
    output_dir="../output/ankidroid/4951/mutate_new",
    policy_name="mutate"
)
run_android_check_as_test(t,setting)

