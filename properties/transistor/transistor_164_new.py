import sys
sys.path.append("..")
from kea import *

class Test(KeaTest):
    

    @initializer()
    def set_up(self):
        d(text="Settings").click()
        
        d(scrollable=True).scroll.to(text="Edit Stations")
        
        d(text="Edit Stations").click()
        
        d.press("back")
        
        for _ in range(3):
            d(text="Add new station").click()
            
            station_name_prefix = ["bbc", "new", "swi","chn"]
            selected_station_name_prefix = random.choice(station_name_prefix)
            d(resourceId="org.y20k.transistor:id/search_src_text").set_text(selected_station_name_prefix)
            time.sleep(3)
            random_selected_station = random.choice(d(resourceId="org.y20k.transistor:id/station_name"))
            random_selected_station.click()
            
            d(text="Add").click()
            
    # 164
    @precondition(
        lambda self: d(resourceId="org.y20k.transistor:id/player_play_button").exists()
    )
    @rule()
    def station_name_should_be_consistent(self):
        station_name = d(resourceId="org.y20k.transistor:id/player_station_name").get_text()
        print("station_name: " + station_name)
        d(resourceId="org.y20k.transistor:id/player_play_button").click()
        time.sleep(2)
        assert d(resourceId="org.y20k.transistor:id/player_station_name",text=station_name).exists(), "NAME changes after playback"



if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/transistor/4.1.7.apk",
        device_serial="emulator-5554",
        output_dir="../output/transistor/164/guided_new",
        policy_name="guided",
        
        number_of_events_that_restart_app = 100
    )
    start_kea(t,setting)
    
