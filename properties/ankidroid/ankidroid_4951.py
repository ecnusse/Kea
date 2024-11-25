import sys
sys.path.append("..")
from kea.core import *

class Test(Kea):

    @mainPath()
    def rule_allow_permission_three_points_exists_mainpath(self):
        d(text="Allow").click()

    @precondition(
        lambda self: d(text="AnkiDroid").exists() and
        d(resourceId="com.ichi2.anki:id/fab_expand_menu_button").exists() and 
        d(resourceId="com.ichi2.anki:id/deckpicker_name").exists()
    )
    @rule()
    def rule_allow_permission_three_points_exists(self):
        
        assert d(description="More options").exists()
        


if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/ankidroid/2.9alpha29.apk",
        device_serial="emulator-5554",
        output_dir="../output/ankidroid/4951/mutate",
        policy_name="mutate",
        grant_perm=False
    )
    start_kea(t,setting)
    
