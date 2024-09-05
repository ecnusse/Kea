import string
from kea.main import *
import time
import sys
import re

class Test(Kea):
    

    @initialize()
    def set_up(self):
        d(resourceId="net.gsantner.markor:id/next").click()
        
        d(resourceId="net.gsantner.markor:id/next").click()
        
        d(resourceId="net.gsantner.markor:id/next").click()
        
        d(resourceId="net.gsantner.markor:id/next").click()
        
        d(text="DONE").click()
        
        
        if d(text="OK").exists():
            d(text="OK").click()
           
    # 1137
    @precondition(
        lambda self: d(resourceId="net.gsantner.markor:id/action_edit").exists()
        )
    @rule()
    def rotation_should_keep_view_mode(self):
        d.set_orientation("l")
        
        d.set_orientation("n")
        
        assert d(resourceId="net.gsantner.markor:id/action_edit").exists()




t = Test()

setting = Setting(
    apk_path="./apk/markor/2.11.1.apk",
    device_serial="emulator-5554",
    output_dir="output/markor/1137/mutate/1",
    policy_name="random",

    main_path="main_path/markor/1137_new.json"
)
run_android_check_as_test(t,setting)

