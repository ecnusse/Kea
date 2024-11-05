import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    
    @initialize()
    def set_up(self):
        d(text="Add a new station").click()
        
        d(className="android.widget.EditText").set_text("http://st01.dlf.de/dlf/01/128/mp3/stream.mp3")
        
        d(text="ADD").click()
        

        d(text="Add a new station").click()
        
        d(className="android.widget.EditText").set_text("http://stream.live.vc.bbcmedia.co.uk/bbc_world_service")
        
        d(text="ADD").click()
        

        d(text="Add a new station").click()
        
        d(className="android.widget.EditText").set_text("http://www.101smoothjazz.com/101-smoothjazz.m3u")
        
        d(text="ADD").click()
        
    @precondition(
        lambda self: d(resourceId="org.y20k.transistor:id/player_playback_button").exists()
    )
    @rule()
    def station_name_should_be_consistent(self):
        station_name = d(resourceId="org.y20k.transistor:id/player_station_name").get_text()
        print("station_name: " + station_name)
        d(resourceId="org.y20k.transistor:id/player_playback_button").click()
        
        assert d(resourceId="org.y20k.transistor:id/player_station_name",text=station_name).exists(), "NAME changes after playback"



t = Test()

setting = Setting(
    apk_path="./apk/transistor/3.0.2.apk",
    device_serial="emulator-5554",
    output_dir="output/transistor/164/mutate/1",
    policy_name="random",

    main_path="main_path/transistor/164.json"
)
start_kea(t,setting)

