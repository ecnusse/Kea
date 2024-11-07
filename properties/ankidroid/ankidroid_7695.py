import sys
sys.path.append("..")
from kea.main import *

class Test(Kea):

    @main_path()
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



t = Test()

setting = Setting(
    apk_path="./apk/ankidroid/2.13.5.apk",
    device_serial="emulator-5554",
    output_dir="../output/ankidroid/7695/mutate",
    policy_name="mutate"
)
start_kea(t,setting)

