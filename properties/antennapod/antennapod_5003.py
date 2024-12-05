import sys
sys.path.append("..")
from kea.core import *

class Test(Kea):
    

    @initializer()
    def set_up(self):
        d.press("back")

    @mainPath()
    def remove_podcast_should_close_miniplayed_mainpath(self):
        d(description="Open menu").click()
        d(text="Add Podcast",resourceId="de.danoeh.antennapod:id/txtvTitle").click()
        d(resourceId="de.danoeh.antennapod.debug:id/discovery_cover").click()
        d(text="Subscribe").click()
        d(resourceId="de.danoeh.antennapod.debug:id/status").click()
        d(resourceId="de.danoeh.antennapod.debug:id/butAction1Text").click()
        d(resourceId="de.danoeh.antennapod.debug:id/playerFragment").click()

    @precondition(
        lambda self: d(resourceId="de.danoeh.antennapod.debug:id/add_to_favorites_item").exists() and 
        d(description="Audio controls") and 
        d(resourceId="de.danoeh.antennapod.debug:id/sbPosition").exists()
    )
    @rule()
    def remove_podcast_should_close_miniplayed(self):
        title = d(resourceId="de.danoeh.antennapod.debug:id/txtvEpisodeTitle").get_text()
        print("title: " + title)
        d(description="More options").click()
        
        d(text="Open Podcast").click()
        
        d(description="More options").click()
        
        d(text="Remove podcast").click()
        
        d(text="Confirm").click()
        time.sleep(3)
        assert not d(resourceId="de.danoeh.antennapod.debug:id/txtvAuthor").exists() and not d(resourceId="de.danoeh.antennapod.debug:id/butPlay").exists(), "miniplayer not closed"
        


if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/antennapod/2.2.0-beta1.apk",
        device_serial="emulator-5554",
        output_dir="../output/antennapod/5003/guided",
        policy_name="guided"
    )
    start_kea(t,setting)
    
