import random
import sys
from itertools import count

sys.path.append("..")
from kea import *

class Test(KeaTest):

    @mainPath()
    def change_setting_should_not_influence_Download_function_mainpath(self):
        d(description="Open menu").click()
        d(text="Add podcast").click()
        d(text="Show suggestions").click()
        d(resourceId="de.danoeh.antennapod:id/discovery_cover").click()
        d(text="Subscribe").click()
        d(resourceId="de.danoeh.antennapod:id/txtvTitle")[random.randint(1, d(resourceId="de.danoeh.antennapod:id/txtvTitle").count - 1)].click()

    @precondition(
        lambda self: d(text="Download").exists() and 
        d(text="Stream").exists() and not
        d(resourceId="de.danoeh.antennapod:id/butFF").exists()
    )
    @rule()
    def change_setting_should_not_influence_Download_function(self):
        d(text="Download").click()
        
        assert d(text="Delete").exists() or d(text="Cancel download").exists()



if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/antennapod/3.2.0.apk",
        device_serial="emulator-5554",
        output_dir="../output/antennapod/3786/guided_new",
        policy_name="guided"
    )
    start_kea(t,setting)
    
