import sys
sys.path.append("..")
from kea import *

class Test(KeaTest):
    

    @initializer()
    def set_up(self):
        if not d(text="Setting").exists() and d(description="Open menu").exists():
            d(description="Open menu").click()

    @mainPath()
    def search_in_one_podcast_should_not_display_others_mainpath(self):
        d(resourceId="de.danoeh.antennapod.debug:id/txtvTitle", text="Add Podcast").click()
        d(resourceId="de.danoeh.antennapod.debug:id/discovery_cover").click()
        d(text="Subscribe").click()
        d(resourceId="de.danoeh.antennapod.debug:id/action_search").click()
        d(resourceId="de.danoeh.antennapod.debug:id/search_src_text").set_text("a")
        d.press("enter")

    @precondition(
        lambda self: d(resourceId="de.danoeh.antennapod.debug:id/discovery_cover").exists() and
          d(resourceId="de.danoeh.antennapod.debug:id/search_src_text").exists() and 
          d(resourceId="de.danoeh.antennapod.debug:id/coverHolder").exists()
    )
    @rule()
    def search_in_one_podcast_should_not_display_others(self):
        assert int(d(resourceId="de.danoeh.antennapod.debug:id/discovery_cover").count) == 1, "discovery cover count not 1"



if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/antennapod/2.0.0.apk",
        device_serial="emulator-5554",
        output_dir="../output/antennapod/4488/guided",
        policy_name="guided"
    )
    start_kea(t,setting)
    
