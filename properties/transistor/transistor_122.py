import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    
    @initialize()
    def set_up(self):
        d(description="Add").click()
        
        d(className="android.widget.EditText").set_text("http://st01.dlf.de/dlf/01/128/mp3/stream.mp3")
        
        d(text="ADD").click()
        
        d(description="Add").click()
        
        d(className="android.widget.EditText").set_text("http://stream.live.vc.bbcmedia.co.uk/bbc_world_service")
        
        d(text="ADD").click()
        
        d(description="Add").click()
        
        d(className="android.widget.EditText").set_text("http://www.101smoothjazz.com/101-smoothjazz.m3u")
        
        d(text="ADD").click()
        
    @precondition(
        lambda self: d(text="Now Playing").exists() and 
        d(resourceId="org.y20k.transistor:id/player_textview_station_metadata").exists()
    )
    @rule()
    def exit_app_and_start_again_shouldnot_change_state(self):
        play_text = d(resourceId="org.y20k.transistor:id/player_textview_station_metadata").get_text()
        print("play_text: " + play_text)
        d.press("recent")
        
        d.press("back")
        
        assert d(resourceId="org.y20k.transistor:id/player_textview_station_metadata").get_text() == play_text, "exit app and start again should not change state"




t = Test()

setting = Setting(
    apk_path="./apk/transistor/4.1.7.apk",
    device_serial="emulator-5554",
    output_dir="output/transistor/122/mutate/1",
    policy_name="random",

    main_path="main_path/transistor/122.json"
)
run_android_check_as_test(t,setting)

