import sys
sys.path.append("..")
from kea import *

class Test(KeaTest):
     
    @initializer()
    def set_up(self):
        d(text="Get Started").click()

    @mainPath()
    def back_should_navigate_to_last_page_mainpath(self):
        d(description="Navigate up").click()
        d(text="Settings").click()
        d(text="Appearance").click()

    # 4935
    @precondition(
        lambda self: d(text="General").exists() and
        d(text="Appearance").exists()
        )
    @rule()
    def back_should_navigate_to_last_page(self):
        d(text="Appearance").click()

        d.press("back")
        
        assert d(text="General").exists()
        


if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/ankidroid/2.18alpha6.apk",
        device_serial="emulator-5554",
        output_dir="output/ankidroid/4935/guided_new/1",
        policy_name="random"
    )
    start_kea(t,setting)
    
