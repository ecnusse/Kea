import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):

    @initialize()
    def set_up(self):
        d(text="Settings").click()
        
        d(scrollable=True).scroll.to(text="Edit Stations")
        
        d(text="Edit Stations").click()
        
        d.press("back")

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
        



t = Test()

setting = Setting(
    apk_path="./apk/transistor/4.1.7.apk",
    device_serial="emulator-5554",
    output_dir="output/transistor/9/1",
    policy_name="random",
    timeout=86400,
    number_of_events_that_restart_app = 100,
    main_path="main_path/transistor/9_new.json",
    run_initial_rules_after_every_mutation=False
)

