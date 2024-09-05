import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @initialize()
    def set_up(self):
        d(text="Add a new station").click()
        
        d(className="android.widget.EditText").set_text("http://stream.live.vc.bbcmedia.co.uk/bbc_world_service")
        
        d(text="ADD").click()
        
    
    @precondition(
        lambda self: d(resourceId="org.y20k.transistor:id/list_item_playback_indicator").exists() and d(resourceId="org.y20k.transistor:id/player_sheet_timer_button").exists()
    )
    @rule()
    def timer_can_be_started_when_playback_are_started(self):
        d(resourceId="org.y20k.transistor:id/player_sheet_timer_button").click()
        
        assert d(resourceId="org.y20k.transistor:id/snackbar_text").exists(), "timer can not be started when playback are started"




t = Test()

setting = Setting(
    apk_path="./apk/transistor/3.0.0.apk",
    device_serial="emulator-5554",
    output_dir="output/transistor/173/mutate/1",
    policy_name="random",

    main_path="main_path/transistor/173.json"
)
run_android_check_as_test(t,setting)

