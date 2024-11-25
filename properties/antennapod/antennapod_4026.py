import sys
sys.path.append("..")
from kea.core import *

class Test(Kea):
    

    @initializer()
    def set_up(self):
        d.press("back")

    @mainPath()
    def play_episode_should_add_to_queue_mainpath(self):
        d(description="Open menu").click()
        d(text="Add Podcast", resourceId="de.danoeh.antennapod.debug:id/txtvTitle").click()
        d(resourceId="de.danoeh.antennapod.debug:id/discovery_cover").click()
        d(text="SUBSCRIBE").click()
        d(resourceId="de.danoeh.antennapod.debug:id/status").click()
        d(resourceId="de.danoeh.antennapod.debug:id/butAction1Text").click()
        d.press("back")
        d(description="Open menu").click()
        d(text="Queue").click()

    @precondition(
        lambda self: d(text="Queue").exists() and 
        d(resourceId="de.danoeh.antennapod.debug:id/queue_lock").exists() and
        d(resourceId="de.danoeh.antennapod.debug:id/txtvTitle").exists() and
        d(resourceId="de.danoeh.antennapod.debug:id/audioplayerFragment").exists() and not
        d(text="Settings").exists()
    )
    @rule()
    def play_episode_should_add_to_queue(self):
        title = d(resourceId="de.danoeh.antennapod.debug:id/audioplayerFragment").child(resourceId="de.danoeh.antennapod.debug:id/txtvTitle").get_text()
        print("title: " + title)
        assert not d(resourceId="de.danoeh.antennapod.debug:id/emptyViewTitle").exists(), "Queue is empty"
        assert d(resourceId="de.danoeh.antennapod.debug:id/recyclerView").child(text=title).exists() and d(scrollable=True,resourceId="de.danoeh.antennapod.debug:id/recyclerView").scroll.to(text=title), "Episode is not in queue"

        



if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/antennapod/2.0.0-alpha1.apk",
        device_serial="emulator-5554",
        output_dir="../output/antennapod/4026/mutate",
        policy_name="mutate"
    )
    start_kea(t,setting)
    
