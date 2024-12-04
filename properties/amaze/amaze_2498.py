import sys
sys.path.append("..")
from kea.core import *

class Test(Kea):
    

    @initializer()
    def set_up(self):
        if d(text="ALLOW").exists():
            d(text="ALLOW").click()
            
        elif d(text="Allow").exists():
            d(text="Allow").click()

    @mainPath()
    def click_sort_should_work_mainpath(self):
        d(description="Navigate up").click()
        d(scrollable = True).scroll.to(text="App Manager")
        d(text="App Manager").click()

    @precondition(lambda self: d(text="App Manager").exists() and 
                  d(description="More options").exists() and not 
                  d(text="Settings").exists())
    @rule()
    def click_sort_should_work(self):
        
        d(resourceId="com.amaze.filemanager.debug:id/sort").click()
        
        
        assert d(text="Sort By").exists()
    



if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/amaze/amaze-9c8048a.apk",
        device_serial="emulator-5554",
        output_dir="../output/amaze/2498/guided/1",
        policy_name="random"
    )
    start_kea(t,setting)
    
