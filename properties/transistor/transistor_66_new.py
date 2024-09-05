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
        
        for _ in range(3):
            d(text="Add new station").click()
            
            station_name_prefix = ["bbc", "new", "swi","chn"]
            selected_station_name_prefix = random.choice(station_name_prefix)
            d(resourceId="org.y20k.transistor:id/search_src_text").set_text(selected_station_name_prefix)
            time.sleep(3)
            random_selected_station = random.choice(d(resourceId="org.y20k.transistor:id/station_name"))
            random_selected_station.click()
            
            d(text="Add").click()
            
    # 66
    @precondition(
        lambda self: d(resourceId="org.y20k.transistor:id/station_name").exists() and not 
        d(text="Save Changes").exists()
    )
    @rule()
    def rename_station_should_work(self):
        original_station_count = int(d(resourceId="org.y20k.transistor:id/station_card").count)
        print("original_station_count: " + str(original_station_count))
        random_selected_station = random.choice(d(resourceId="org.y20k.transistor:id/station_name"))
        print("random_selected_station: " + random_selected_station.get_text())
        random_selected_station.long_click()
        
        new_name = st.text(alphabet=string.ascii_lowercase,min_size=1, max_size=5).example()
        d(resourceId="org.y20k.transistor:id/edit_station_name").set_text(new_name)
        
        d(text="Save Changes").click()
        
        new_station_count = int(d(resourceId="org.y20k.transistor:id/station_card").count)
        assert new_station_count >= original_station_count, "station count changed"



t = Test()

setting = Setting(
    apk_path="./apk/transistor/4.1.7.apk",
    device_serial="emulator-5554",
    output_dir="output/transistor/66/1",
    policy_name="random",

    run_initial_rules_after_every_mutation=False,
    main_path="main_path/transistor/66_new.json"
)
run_android_check_as_test(t,setting)

