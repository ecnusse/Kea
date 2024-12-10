import string
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

    # 44
    @precondition(
        lambda self: d(resourceId="org.y20k.transistor:id/player_station_name").exists() and 
        d(resourceId="org.y20k.transistor:id/station_name", text=d(resourceId="org.y20k.transistor:id/player_station_name").get_text()).exists() and not
        d(text="Save Changes").exists()
    )
    @rule()
    def rename_station_not_change_station_state(self):
        playing_station_name = d(resourceId="org.y20k.transistor:id/player_station_name").get_text()
        print("playing_station_name: " + playing_station_name)
        d(resourceId="org.y20k.transistor:id/station_name", text=playing_station_name).long_click()
        
        new_name = st.text(alphabet=string.ascii_lowercase,min_size=1, max_size=5).example()
        print("new_name: " + new_name)
        d(resourceId="org.y20k.transistor:id/edit_station_name").set_text(new_name)
        time.sleep(2)
        d(text="Save Changes").click()
        
        assert d(resourceId="org.y20k.transistor:id/station_name", text=new_name).exists(), "NEW NAME DOES NOT EXIST in station"
        assert d(resourceId="org.y20k.transistor:id/player_station_name", text=new_name).exists(), "NEW NAME DOES NOT EXIST in player"
        assert not d(resourceId="org.y20k.transistor:id/station_name", text=playing_station_name).exists(), "OLD NAME STILL EXISTS"
        


if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/transistor/4.1.7.apk",
        device_serial="emulator-5554",
        output_dir="../output/transistor/44/guided_new",
        policy_name="guided",
        timeout=43200,
        number_of_events_that_restart_app = 100,
        # run_initial_rules_after_every_mutation=False
    )
    start_kea(t,setting)
    
