import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @initialize()
    def set_up(self):
        d(description="Open menu").click()
        
        d(text="Add podcast").click()
        
        if d(text="Show suggestions").exists():
            d(text="Show suggestions").click()
            
        random.choice(d(resourceId="de.danoeh.antennapod:id/discovery_cover")).click()
        time.sleep(3)
        d(text="Subscribe").click()

    @precondition(
        lambda self: d(text="Episodes").exists() and 
        d(resourceId="de.danoeh.antennapod:id/container").exists() 
    )
    @rule()
    def delete_should_update_the_filter_episodes(self):
        
        d(description="More options").click()
        
        d(text="Filter").click()
        
        d(text="Reset").click()
        
        d(text="Downloaded").click()
        
        d.press("back")
        
        if not d(resourceId="de.danoeh.antennapod:id/container").exists():
            print("no episodes found")
            return
        title = d(resourceId="de.danoeh.antennapod:id/txtvTitle").get_text()
        print("title: " + title)
        d(resourceId="de.danoeh.antennapod:id/txtvTitle").long_click()
        
        d(text="Delete").click()
        
        assert not d(text=title).exists(), "episode not deleted"



t = Test()

setting = Setting(
    apk_path="./apk/antennapod/3.3.2.apk",
    device_serial="emulator-5554",
    output_dir="output/antennapod/4548/mutate_new/1",
    policy_name="random",

    main_path="main_path/antennapod/4548_new.json"
)
run_android_check_as_test(t,setting)

