import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    
        
    @initialize()
    def set_up(self):
        if d(text="Allow").exists():
            d(text="Allow").click()
            
        if d(text="GRANT").exists():
            d(text="GRANT").click()

    # 2128
    @precondition(lambda self:  d(text="Amaze").exists() and 
                  d(resourceId="com.amaze.filemanager:id/fullpath").exists() and not 
                  d(resourceId="com.amaze.filemanager:id/item_count").exists() and 
                  d(resourceId="com.amaze.filemanager:id/search").exists() and not
                  d(resourceId="com.amaze.filemanager:id/search_edit_text").exists() and 
                  "/" in d(resourceId="com.amaze.filemanager:id/fullpath").get_text() 
                  ) 
    @rule()
    def rule_FAB_should_appear(self):
        
        assert d(resourceId="com.amaze.filemanager:id/sd_main_fab").exists(), "FAB should appear"

    




t = Test()

setting = Setting(
    apk_path="./apk/amaze/3.10.apk",
    device_serial="emulator-5554",
    output_dir="output/amaze/2128/1",
    policy_name="random",

    main_path="main_path/amaze/2128_new.json"
)
start_kea(t,setting)

