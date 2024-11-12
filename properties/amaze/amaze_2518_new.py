import sys
sys.path.append("..")
from kea.main import *

class Test(Kea):

    @initializer()
    def set_up(self):
        if d(text="GRANT").exists():
            d(text="GRANT").click()

        elif d(text="Grant").exists():
            d(text="Grant").click()

        if d(text="ALLOW").exists():
            d(text="ALLOW").click()

        elif d(text="Allow").exists():
            d(text="Allow").click()

    @mainPath()
    def click_exist_button_should_work_mainpath(self):
        d(description="Navigate up").click()
        d(scrollable=True).scroll.to(text="App Manager")
        d(text="App Manager").click()

    @precondition(lambda self: d(text="App Manager").exists() and d(description="More options").exists())
    @rule()
    def click_exist_button_should_work(self):
        
        d(description="More options").click()
        
        d(text="Exit").click()
        
        assert not d(text="App Manager").exists()
    



if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/amaze/amaze-3.8.4.apk",
        device_serial="emulator-5554",
        output_dir="../output/amaze/2518/mutate_new",
        policy_name="mutate"
    )
    start_kea(t,setting)
    
