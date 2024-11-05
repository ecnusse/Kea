import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @initialize()
    def set_up(self):
        d.press("back")

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
        


t = Test()

setting = Setting(
    apk_path="./apk/antennapod/2.2.0-beta1.apk",
    device_serial="emulator-5554",
    output_dir="output/antennapod/5003/mutate/1",
    policy_name="random",

    main_path="main_path/antennapod/5003.json"
)
start_kea(t,setting)

