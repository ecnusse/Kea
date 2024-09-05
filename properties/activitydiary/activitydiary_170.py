import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @precondition(
        lambda self: d(text="Settings").exists() and d(text="Import database").exists()
    )
    @rule()
    def import_an_backup_should_take_effect(self):
        
        d(text="Import database").click()
        
        d(description="Show roots").click()
        
        d(text="Downloads",resourceId="android:id/title").click()
        
        d(text="ActivityDiary_Export.sqlite3").click()
        
        d.press("back")
        
        assert d(text="A").exists(), "A not exists"



t = Test()

setting = Setting(
    apk_path="./apk/activitydiary/1.2.5.apk",
    device_serial="emulator-5554",
    output_dir="output/activitydiary/170/mutate/1",
    policy_name="random",

    main_path="main_path/activitydiary/170.json"
)
run_android_check_as_test(t,setting)

