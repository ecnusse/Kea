import sys
sys.path.append("..")
from kea import *

class Test(KeaTest):
    

    @initializer()
    def set_up(self):
        if d(text="ALLOW").exists():
            d(text="ALLOW").click()
            
        elif d(text="Allow").exists():
            d(text="Allow").click()

    @mainPath()
    def back_should_not_go_to_main_setting_mainpath(self):
        d(description="Navigate up").click()
        d(scrollable = True).scroll.to(text="Settings")
        d(text="Settings").click()
        d(text="Color").click()
        d(text="Select color config").click()

    @precondition(lambda self: d(text="Color").exists() and d(text="Customize").exists())
    @rule()
    def back_should_not_go_to_main_setting(self):
        
        d(description="Navigate up").click()
        
        assert not d(text="Settings").exists()
    


if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/amaze/amaze-b7c9c81.apk",
        device_serial="emulator-5554",
        output_dir="../output/amaze/2477/guided/1",
        policy_name="random"
    )
    start_kea(t,setting)
    
