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
            

    @precondition(lambda self: d(textContains=".zip").exists() and not 
                  d(text="Internal Storage").exists())
    @rule()
    def extract_zip_file_shouldnot_need_password(self):
        
        zip_file = d(textContains=".zip")
        folder_name = zip_file.get_text().split(".")[0]
        print("zip_file: "+str(zip_file.get_text()))
        zip_file.click()
        
        d(text="EXTRACT").click()
        
        assert d(text=folder_name).exists(), "extract zip file failed with zip file name: "+str(zip_file.get_text())




t = Test()

setting = Setting(
    apk_path="./apk/amaze/amaze-3.4.2.apk",
    device_serial="emulator-5554",
    output_dir="output/amaze/1834/mutate/1",
    policy_name="random",

    main_path="main_path/amaze/1834.json"
)
run_android_check_as_test(t,setting)

