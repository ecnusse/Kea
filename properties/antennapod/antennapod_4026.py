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

        



t = Test()

setting = Setting(
    apk_path="./apk/antennapod/2.0.0-alpha1.apk",
    device_serial="emulator-5554",
    output_dir="output/antennapod/4026/mutate/1",
    policy_name="random",

    main_path="main_path/antennapod/4026.json"
)
run_android_check_as_test(t,setting)

