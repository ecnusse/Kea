import sys
sys.path.append("..")
from kea.core import *

class Test(Kea):

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
            
    # 234
    @precondition(
        lambda self: d(resourceId="org.y20k.transistor:id/station_card").exists()
    )
    @rule()
    def cancel_delete_should_not_change_name(self):
        random_selected_station = random.choice(d(resourceId="org.y20k.transistor:id/station_card"))
        station_name = random_selected_station.child(resourceId="org.y20k.transistor:id/station_name").get_text()
        print("station_name: " + station_name)
        random_selected_station.fling.horiz.toEnd(max_swipes=1000)
        
        d(text="Cancel").click()
        
        assert d(text=station_name).exists(), "NAME changes after cancel delete"



if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/transistor/4.1.7.apk",
        device_serial="emulator-5554",
        output_dir="../output/transistor/239/mutate_new",
        policy_name="mutate",
        # run_initial_rules_after_every_mutation=False
    )
    start_kea(t,setting)
    
