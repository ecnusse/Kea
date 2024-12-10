import sys
sys.path.append("..")
from kea import *

class Test(KeaTest):
    

    @initializer()
    def set_up(self):
        d.press("back")

    @mainPath()
    def click_podcast_should_work_mainpath(self):
        d(description="Open menu").click()
        d(text="Add Podcast", resourceId="de.danoeh.antennapod.debug:id/txtvTitle").click()
        d(resourceId="de.danoeh.antennapod.debug:id/discovery_cover").click()
        d(text="SUBSCRIBE").click()
        d(resourceId="de.danoeh.antennapod.debug:id/status").click()
        d(resourceId="de.danoeh.antennapod.debug:id/butAction1Text").click()
        d(resourceId="de.danoeh.antennapod.debug:id/playerFragment").click()

    @precondition(
        lambda self: d(resourceId="de.danoeh.antennapod.debug:id/butPlay").exists() and 
        d(description="More options").exists() and 
        d(resourceId="de.danoeh.antennapod.debug:id/add_to_favorites_item").exists()
    )
    @rule()
    def click_podcast_should_work(self):
        d(description="More options").click() 
        
        d(text="Open Podcast").click()
        
        assert not d(resourceId="de.danoeh.antennapod.debug:id/butFF").exists()



if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/antennapod/2.0.0-alpha1.apk",
        device_serial="emulator-5554",
        output_dir="../output/antennapod/4010/guided",
        policy_name="guided"
    )
    start_kea(t,setting)
    
