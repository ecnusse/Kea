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

    @precondition(
        lambda self: d(resourceId="org.y20k.transistor:id/station_card").exists() and d(resourceId="org.y20k.transistor:id/station_card").count > 1 and d(resourceId="org.y20k.transistor:id/player_play_button").exists()
    )
    @rule()
    def notification_button_should_work(self):
        station_name = d(resourceId="org.y20k.transistor:id/player_station_name").get_text()
        print("station_name: " + station_name)
        d(resourceId="org.y20k.transistor:id/player_play_button").click()
        time.sleep(2)
        d.open_notification()
        
        if not d(resourceId="android:id/action2").exists():
            d.press("back")
            return
        d(resourceId="android:id/action2").click()
        
        d.press("back")
        
        new_station_name = d(resourceId="org.y20k.transistor:id/player_station_name").get_text()
        print("new_station_name: " + new_station_name)
        assert station_name != new_station_name, "notification next button does not work"



if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/transistor/4.1.7.apk",
        device_serial="emulator-5554",
        output_dir="../output/transistor/363/guided_new",
        policy_name="guided",
        timeout=86400,
        number_of_events_that_restart_app = 100
    )
    start_kea(t,setting)
    
