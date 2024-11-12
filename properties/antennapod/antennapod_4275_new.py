import sys
sys.path.append("..")
from kea.main import *

class Test(Kea):

    @mainPath()
    def play_video_should_not_play_as_audio_mainpath(self):
        d(resourceId="de.danoeh.antennapod:id/combinedFeedSearchBox").set_text("look at book")
        d.press("enter")
        d(text="Look at the Book").click()
        d(text="Subscribe").click()
        d(description="Download").click()
        d.wait(timeout=20)

    @precondition(
        lambda self: d(resourceId="de.danoeh.antennapod:id/butShowInfo").exists() and 
        d(resourceId="de.danoeh.antennapod:id/ivIsVideo").exists() and
        d(description="Play").exists()
    )
    @rule()
    def play_video_should_not_play_as_audio(self):
        d(description="Play").click()
        
        assert d(resourceId="de.danoeh.antennapod:id/videoPlayerContainer").exists()




if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/antennapod/3.2.0.apk",
        device_serial="emulator-5554",
        output_dir="../output/antennapod/4275/mutate_new",
        policy_name="mutate",
        
        number_of_events_that_restart_app = 100
    )
    start_kea(t,setting)
    
