import sys
sys.path.append("..")
from kea.core import *

class Test(Kea):
    
    @initializer()
    def set_up(self):
        d(text="ADD NEW STATION").click()
        
        d(className="android.widget.EditText").set_text("http://st01.dlf.de/dlf/01/128/mp3/stream.mp3")
        
        d(text="ADD").click()

        d(text="ADD NEW STATION").click()
        
        d(className="android.widget.EditText").set_text("http://www.101smoothjazz.com/101-smoothjazz.m3u")
        
        d(text="ADD").click()

        d(text="ADD NEW STATION").click()
        
        d(className="android.widget.EditText").set_text("http://stream.live.vc.bbcmedia.co.uk/bbc_world_service")
        
        d(text="ADD").click()

    @precondition(
        lambda self: d(resourceId="org.y20k.transistor:id/station_card").exists() and d(resourceId="org.y20k.transistor:id/station_card").count > 1 and d(resourceId="org.y20k.transistor:id/player_play_button").exists()
    )
    @rule()
    def notification_button_should_work(self):
        station_name = d(resourceId="org.y20k.transistor:id/player_station_name").get_text()
        print("station_name: " + station_name)
        d(resourceId="org.y20k.transistor:id/player_play_button").click()
        
        d.open_notification()
        
        if not d(description="Next").exists():
            d.press("back")
            return
        d(description="Next").click()
        
        d.press("back")
        
        new_station_name = d(resourceId="org.y20k.transistor:id/player_station_name").get_text()
        print("new_station_name: " + new_station_name)
        assert station_name != new_station_name, "notification next button does not work"



if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/transistor/4.0.15.apk",
        device_serial="emulator-5554",
        output_dir="../output/transistor/363/mutate",
        policy_name="mutate"
    )
    start_kea(t,setting)
    
