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



t = Test()

setting = Setting(
    apk_path="./apk/antennapod/2.0.1.apk",
    device_serial="emulator-5554",
    output_dir="output/antennapod/4548/mutate/1",
    policy_name="random",

    main_path="main_path/antennapod/4548.json"
)
start_kea(t,setting)

