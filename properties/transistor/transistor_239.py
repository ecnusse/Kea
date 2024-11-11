import sys
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @initializer()
    def set_up(self):
        d(text="Add a new station").click()
        
        d(className="android.widget.EditText").set_text("http://st01.dlf.de/dlf/01/128/mp3/stream.mp3")
        
        d(text="ADD").click()
        

        d(text="Add a new station").click()
        
        d(className="android.widget.EditText").set_text("http://www.101smoothjazz.com/101-smoothjazz.m3u")
        
        d(text="ADD").click()
        

        d(text="Add a new station").click()
        
        d(className="android.widget.EditText").set_text("http://stream.live.vc.bbcmedia.co.uk/bbc_world_service")
        
        d(text="ADD").click()

    @mainPath()
    def delete_should_work_mainpath(self):
        d(resourceId="org.y20k.transistor:id/player_station_name", text="stream").swipe("up", steps=20)

    @precondition(
        lambda self: d(resourceId="org.y20k.transistor:id/player_sheet_station_options_button").exists()
    )
    @rule()
    def delete_should_work(self):
        station_name = d(resourceId="org.y20k.transistor:id/player_station_name").get_text()
        print("station_name: " + station_name)
        d(resourceId="org.y20k.transistor:id/player_sheet_station_options_button").click()
        
        d(text="Delete").click()
        
        d(text="DELETE").click()
        
        assert not d(text=station_name).exists(), "delete does not work"



if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/transistor/3.2.2.apk",
        device_serial="emulator-5554",
        output_dir="../output/transistor/239/mutate",
        policy_name="mutate"
    )
    start_kea(t,setting)
    
