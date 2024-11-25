import sys
sys.path.append("..")
from kea.core import *

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
    def search_in_one_podcast_should_not_display_others_mainpath(self):
        d(resourceId="de.danoeh.antennapod:id/action_search").click()
        d(resourceId="de.danoeh.antennapod:id/search_src_text").set_text("a")
        d.press("enter")


    @precondition(
        lambda self: d(resourceId="de.danoeh.antennapod:id/container").exists() and
          d(resourceId="de.danoeh.antennapod:id/search_src_text").exists() and 
          d(resourceId="de.danoeh.antennapod:id/feed_title_chip").exists()
    )
    @rule()
    def search_in_one_podcast_should_not_display_others(self):
        podcast_name = d(resourceId="de.danoeh.antennapod:id/feed_title_chip").get_text()
        print("podcast name: " + podcast_name)
        random.choice(d(resourceId="de.danoeh.antennapod:id/container")).click()
        name = d(resourceId="de.danoeh.antennapod:id/txtvPodcast").get_text()
        print("name: " + name)
        assert name == podcast_name, "name not equal to podcast name"



if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/antennapod/3.3.2.apk",
        device_serial="emulator-5554",
        output_dir="../output/antennapod/4488/mutate_new",
        policy_name="mutate"
    )
    start_kea(t,setting)
    
