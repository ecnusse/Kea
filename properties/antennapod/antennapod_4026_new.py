import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    
    

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

        



t = Test()

setting = Setting(
    apk_path="./apk/antennapod/3.3.2.apk",
    device_serial="emulator-5554",
    output_dir="output/antennapod/4026/mutate_new/1",
    policy_name="random",
    timeout=86400,
    number_of_events_that_restart_app = 100,
    main_path="main_path/antennapod/4026_new.json"
)
start_kea(t,setting)

