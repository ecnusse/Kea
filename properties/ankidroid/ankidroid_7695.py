import sys
sys.path.append("..")
from kea.core import *

class Test(Kea):

    @mainPath()
    def rename_note_type_shouldnot_display_mainpath(self):
        d(description="More options").click()
        d(text="Manage note types").click()
        d(resourceId="com.ichi2.anki:id/model_list_item_1").click()
        d(text="Front").click()

    @precondition(
        lambda self: d(text="Front").exists() and 
        d(text="Rename field").exists()
    )
    @rule()
    def rename_note_type_shouldnot_display(self):
        
        d(text="Rename field").click()
        
        assert not d(text="Rename note type").exists(), "Rename note type found"



if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/ankidroid/2.13.5.apk",
        device_serial="emulator-5554",
        output_dir="../output/ankidroid/7695/guided",
        policy_name="guided"
    )
    start_kea(t,setting)
    
