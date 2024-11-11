import sys
sys.path.append("..")
from kea.main import *

class Test(Kea):

    @mainPath()
    def play_episode_should_add_to_queue_mainpath(self):
        d(description="Open menu").click()
        d(text="Add podcast").click()
        d(text="Show suggestions").click()
        d(resourceId="de.danoeh.antennapod:id/discovery_cover").click()
        d(text="Subscribe").click()
        d(resourceId="de.danoeh.antennapod:id/progress").click()
        d(resourceId="de.danoeh.antennapod:id/butAction1").click()
        d.press("back")
        d(description="Open menu").click()
        d(text="Queue").click()

    @precondition(
        lambda self: d(text="Queue").exists() and 
        d(resourceId="de.danoeh.antennapod:id/txtvTitle").exists() and
        d(resourceId="de.danoeh.antennapod:id/audioplayerFragment").exists() and not
        d(text="Settings").exists()
    )
    @rule()
    def play_episode_should_add_to_queue(self):
        title = d(resourceId="de.danoeh.antennapod:id/audioplayerFragment").child(resourceId="de.danoeh.antennapod:id/txtvTitle").get_text()
        print("title: " + title)
        assert not d(resourceId="de.danoeh.antennapod:id/emptyViewTitle").exists(), "Queue is empty"
        assert d(resourceId="de.danoeh.antennapod:id/recyclerView").child(text=title).exists() or d(scrollable=True,resourceId="de.danoeh.antennapod:id/recyclerView").scroll.to(text=title), "Episode is not in queue"

        



if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/antennapod/3.3.2.apk",
        device_serial="emulator-5554",
        output_dir="../output/antennapod/4026/mutate_new",
        policy_name="mutate",
        timeout=86400,
        number_of_events_that_restart_app = 100
    )
    start_kea(t,setting)
    
