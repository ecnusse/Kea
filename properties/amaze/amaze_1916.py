import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    
    @initialize()
    def set_up(self):
        if d(text="ALLOW").exists():
            d(text="ALLOW").click()
            
        elif d(text="Allow").exists():
            d(text="Allow").click()
            

    @precondition(lambda self: d(text="Documents").exists()  and not d(text="Settings").exists())
    @rule()
    def rule_documnets(self):
        
        
        assert d(resourceId="com.amaze.filemanager:id/firstline").exists()



t = Test()

setting = Setting(
    apk_path="./apk/amaze/amaze-3.4.3.apk",
    device_serial="emulator-5554",
    output_dir="output/amaze/1916/mutate/1",
    policy_name="random",

    main_path="main_path/amaze/1916.json"
)
run_android_check_as_test(t,setting)

