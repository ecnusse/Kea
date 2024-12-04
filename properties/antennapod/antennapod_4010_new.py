import sys
sys.path.append("..")
from kea.core import *

class Test(Kea):

    @mainPath()
    def click_podcast_should_work_mainpath(self):
        d(description="Open menu").click()
        d(text="Add podcast").click()
        d(text="Show suggestions").click()
        d(resourceId="de.danoeh.antennapod:id/discovery_cover").click()
        d(text="Subscribe").click()
        d(resourceId="de.danoeh.antennapod:id/status").click()
        d(resourceId="de.danoeh.antennapod:id/butAction1Text").click()
        d(resourceId="de.danoeh.antennapod:id/playerFragment").click()

    @precondition(
        lambda self: d(resourceId="de.danoeh.antennapod:id/butPlay").exists() and 
        d(description="More options").exists() and 
        d(resourceId="de.danoeh.antennapod:id/add_to_favorites_item").exists()
    )
    @rule()
    def click_podcast_should_work(self):
        d(description="More options").click() 
        
        d(text="Open podcast").click()
        
        assert not d(resourceId="de.danoeh.antennapod:id/butFF").exists()





if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/antennapod/3.2.0.apk",
        device_serial="emulator-5554",
        output_dir="../output/antennapod/4010/guided_new",
        policy_name="guided",
        
        number_of_events_that_restart_app = 100
    )
    start_kea(t,setting)
    
