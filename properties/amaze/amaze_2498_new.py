import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @precondition(lambda self: d(text="App Manager").exists() and d(description="More options").exists())
    @rule()
    def click_sort_should_work(self):
        
        d(resourceId="com.amaze.filemanager:id/sort").click()
        
        assert d(text="Sort By").exists()
    



t = Test()

setting = Setting(
    apk_path="./apk/3.8.4.apk",
    device_serial="emulator-5554",
    output_dir="output/amaze/2498/1",
    policy_name="random",

)

