import sys
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @initializer()
    def set_up(self):
        d(description="Open menu").click()
        
        d(text="Add podcast").click()
        
        if d(text="Show suggestions").exists():
            d(text="Show suggestions").click()
            
        random.choice(d(resourceId="de.danoeh.antennapod:id/discovery_cover")).click()
        time.sleep(3)
        d(text="Subscribe").click()

    @mainPath()
    def remove_podcast_should_close_miniplayed_mainpath(self):
        d(resourceId="de.danoeh.antennapod:id/txtvTitle")[random.randint(1, d(resourceId="de.danoeh.antennapod:id/txtvTitle").count - 1)].click()
        d(text="Stream").click()
        d(resourceId="de.danoeh.antennapod:id/playerFragment").click()

    @precondition(
        lambda self: d(resourceId="de.danoeh.antennapod:id/add_to_favorites_item").exists() and 
        d(resourceId="de.danoeh.antennapod:id/butPlay") and 
        d(resourceId="de.danoeh.antennapod:id/sbPosition").exists()
    )
    @rule()
    def remove_podcast_should_close_miniplayed(self):
        title = d(resourceId="de.danoeh.antennapod:id/txtvEpisodeTitle").get_text()
        print("title: " + title)
        d(description="More options").click()
        
        d(text="Open podcast").click()
        
        d(description="More options").click()
        
        d(text="Remove podcast").click()
        
        d(text="Confirm").click()
        time.sleep(3)
        assert not d(resourceId="de.danoeh.antennapod:id/audioplayerFragment").exists() , "miniplayer not closed"
        


t = Test()

setting = Setting(
    apk_path="./apk/antennapod/3.3.2.apk",
    device_serial="emulator-5554",
    output_dir="../output/antennapod/5003/mutate_new",
    policy_name="mutate"
)
start_kea(t,setting)

