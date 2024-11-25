import sys
sys.path.append("..")
from kea.core import *

class Test(Kea):
    

    @initializer()
    def set_up(self):
        d.press("back")

    @mainPath()
    def play_video_should_not_play_as_audio_mainpath(self):
        d(resourceId="de.danoeh.antennapod:id/combinedFeedSearchBox").set_text("look at book")
        d.press("enter")
        d(text="Look at the Book").click()
        d(text="SUBSCRIBE").click()
        d(description="Download").click()
        d.wait(timeout=20)

    @precondition(
        lambda self: d(resourceId="de.danoeh.antennapod:id/butShowInfo").exists() and not 
        d(resourceId="de.danoeh.antennapod:id/imgvType").exists() and
        d(description="Play").exists()
    )
    @rule()
    def play_video_should_not_play_as_audio(self):
        d(description="Play").click()
        
        assert not d(resourceId="de.danoeh.antennapod:id/playerFragment").exists()




if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/antennapod/1.8.1.apk",
        device_serial="emulator-5554",
        output_dir="../output/antennapod/4275/mutate",
        policy_name="mutate"
    )
    start_kea(t,setting)
    
