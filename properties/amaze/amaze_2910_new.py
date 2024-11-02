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
    def rotate_should_persist_selected_item_mainpath(self):
        d(resourceId="com.amaze.filemanager:id/firstline").long_click()

    @precondition(lambda self: d(resourceId="com.amaze.filemanager:id/item_count").exists() and d(resourceId="com.amaze.filemanager:id/check_icon").exists() and d(resourceId="com.amaze.filemanager:id/cpy").exists())
    @rule()
    def rotate_should_persist_selected_item(self):
        
        d.set_orientation('l')
        
        d.set_orientation('n')
        
        assert d(resourceId="com.amaze.filemanager:id/check_icon").exists(), "rotate_should_persist_selected_item failed"


t = Test()

setting = Setting(
    apk_path="./apk/amaze/amaze-3.8.4.apk",
    device_serial="emulator-5554",
    output_dir="../output/amaze/2910/mutate_new",
    policy_name="mutate"
)
run_android_check_as_test(t,setting)

