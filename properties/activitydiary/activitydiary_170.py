import sys
sys.path.append("..")
from kea import *

class Test(KeaTest):

    @mainPath()
    def import_an_backup_should_take_effect_mainpath(self):
        d(description="Open navigation").click()
        d(text="Settings").click()
        d(scrollable=True).scroll.to(text="Import database")

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



if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/activitydiary/1.2.5.apk",
        device_serial="emulator-5554",
        output_dir="output/activitydiary/170/guided/1",
        policy_name="random"
    )
    start_kea(t,setting)
    
