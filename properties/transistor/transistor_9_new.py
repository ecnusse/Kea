import sys
sys.path.append("..")
from kea.main import *

class Test(Kea):

    @initializer()
    def set_up(self):
        d(text="Settings").click()
        
        d(scrollable=True).scroll.to(text="Edit Stations")
        
        d(text="Edit Stations").click()
        
        d.press("back")

    @mainPath()
    def should_add_station_mainpath(self):
        d(resourceId="org.y20k.transistor:id/card_add_new_station").click()

    # bug 9
    @precondition(
        lambda self: d(text="Find Station").exists()
    )
    @rule()
    def add_station(self):
        
        station_name_prefix = ["bbc", "new", "swi","chn"]
        selected_station_name_prefix = random.choice(station_name_prefix)
        d(resourceId="org.y20k.transistor:id/search_src_text").set_text(selected_station_name_prefix)
        time.sleep(3)
        random_selected_station = random.choice(d(resourceId="org.y20k.transistor:id/station_name"))
        name = random_selected_station.get_text()
        print("name: " + name)
        random_selected_station.click()
        
        d(text="Add").click()
        time.sleep(2)
        assert d(resourceId="org.y20k.transistor:id/station_name", text=name).exists() or d(scrollable=True).scroll.to(text=name,resourceId="org.y20k.transistor:id/station_name"), "Station not added"
        



if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/transistor/4.1.7.apk",
        device_serial="emulator-5554",
        output_dir="../output/transistor/9/mutate_new",
        policy_name="mutate",
        timeout=86400,
        number_of_events_that_restart_app = 100
    
    )
    
    start_kea(t,setting)
