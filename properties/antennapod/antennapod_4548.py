import sys
sys.path.append("..")
from kea import *

class Test(KeaTest):
    

    @initializer()
    def set_up(self):
        d.press("back")

    @mainPath()
    def delete_should_update_the_filter_episodes_mainpath(self):
        d(description="Open menu").click()
        d(text="Add Podcast", resourceId="de.danoeh.antennapod:id/txtvTitle").click()
        d(resourceId="de.danoeh.antennapod:id/discovery_cover").click()
        d(text="Subscribe").click()
        d(resourceId="de.danoeh.antennapod:id/secondaryActionButton").click()
        d(text="Allow temporarily").click()
        d(description="Open menu").click()
        d(text="Episodes").click()

    @precondition(
        lambda self: d(text="Episodes").exists() and d(text="ALL").exists() and d(resourceId="de.danoeh.antennapod:id/status").exists() and not 
        d(resourceId="de.danoeh.antennapod:id/txtvInformation").exists()
    )
    @rule()
    def delete_should_update_the_filter_episodes(self):
        d(text="ALL").click()
        
        d(description="More options").click()
        
        d(text="Filter").click()
        
        d(text="Downloaded").click()
        
        d(text="Confirm").click()
        
        if not d(resourceId="de.danoeh.antennapod:id/status").exists():
            print("no episodes found")
            return
        title = d(resourceId="de.danoeh.antennapod:id/txtvTitle").get_text()
        print("title: " + title)
        d(resourceId="de.danoeh.antennapod:id/txtvTitle").long_click()
        
        d(text="Delete").click()
        
        assert not d(text=title).exists(), "episode not deleted"



if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/antennapod/2.0.1.apk",
        device_serial="emulator-5554",
        output_dir="../output/antennapod/4548/guided",
        policy_name="guided"
    )
    start_kea(t,setting)
    
