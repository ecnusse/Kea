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
    def should_display_files_mainpath(self):
        d(resourceId="com.amaze.filemanager:id/search").click()
        d(resourceId="com.amaze.filemanager:id/search_edit_text").set_text("data")
        d.press("search")
        d(resourceId="com.amaze.filemanager:id/search").click()
        d(resourceId="com.amaze.filemanager:id/search_edit_text").set_text("data")
        d.press("search")
    
    @precondition(lambda self: d(textContains="Search results").exists())
    @rule()
    def should_display_files(self):
        
        d.set_orientation("l")
        
        d.set_orientation("n")
        
        assert d(textContains="Search results").exists()



t = Test()

setting = Setting(
    apk_path="./apk/amaze/amaze-3.8.4.apk",
    device_serial="emulator-5554",
    output_dir="../output/amaze/1978/mutate/1",
    policy_name="random"
)
start_kea(t,setting)

