import sys
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @precondition(
        lambda self: d(text="考研").exists() and d(text="例句").exists() and 
        d(resourceId="com.ichi2.anki:id/action_sync").exists()
    )
    @rule()
    def should_display_name_of_sub_deck(self):
        d(text="考研").click()
        
        assert d(text="例句").exists(), "例句 not found"



t = Test()

setting = Setting(
    apk_path="./apk/ankidroid/2.14alpha1.apk",
    device_serial="emulator-5554",
    output_dir="../output/ankidroid/7076/mutate",
    policy_name="mutate"
)
run_android_check_as_test(t,setting)

