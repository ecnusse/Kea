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
    def suggestion_should_be_hiden_mainpath(self):
        d(description="Open menu").click()
        d(text="Add podcast").click()
        d(resourceId="de.danoeh.antennapod:id/discover_more").click()
        d(description="More options").click()
        d(text="Hide").click()

    @precondition(
        lambda self: d(text="You selected to hide suggestions.").exists()
    )
    @rule()
    def suggestion_should_be_hiden(self):
        assert not d(text="Suggestions by Apple Podcasts").exists(), "suggestion found"
        



if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/antennapod/3.2.0.apk",
        device_serial="emulator-5554",
        output_dir="../output/antennapod/4669/guided_new",
        policy_name="guided",
        
        number_of_events_that_restart_app = 100
    )
    start_kea(t,setting)
    
