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
    def should_notice_user_when_no_network_mainpath(self):
        d(description="Navigate up").click()
        d(scrollable=True).scroll.to(text="FTP Server")
        d(text="FTP Server").click()

    # 1920
    @precondition(lambda self: d(text="FTP Server").exists() and d(text="START").exists())
    @rule()
    def should_notice_user_when_no_network(self):
        d(text="START").click()
        
        assert d(text="STOP").exists()




if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/amaze/amaze-3.8.4.apk",
        device_serial="emulator-5554",
        output_dir="../output/amaze/1920/random_100/1",
        policy_name="guided",
        
        number_of_events_that_restart_app = 100
    )
    start_kea(t,setting)
    
