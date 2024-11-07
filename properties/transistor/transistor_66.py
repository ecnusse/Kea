import string
import sys
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @initialize()
    def set_up(self):
        d(description="Add").click()
        
        d(className="android.widget.EditText").set_text("http://st01.dlf.de/dlf/01/128/mp3/stream.mp3")
        
        d(text="ADD").click()
        
        d(description="Add").click()
        
        d(className="android.widget.EditText").set_text("http://stream.live.vc.bbcmedia.co.uk/bbc_world_service")
        
        d(text="ADD").click()
        
        d(description="Add").click()
        
        d(className="android.widget.EditText").set_text("http://www.101smoothjazz.com/101-smoothjazz.m3u")
        
        d(text="ADD").click()


    @precondition(
        lambda self: d(resourceId="org.y20k.transistor:id/list_item_more_button").exists()
    )
    @rule()
    def rename_station_should_work(self):
        original_station_count = int(d(resourceId="org.y20k.transistor:id/list_item_textview").count)
        print("original_station_count: " + str(original_station_count))
        d(resourceId="org.y20k.transistor:id/list_item_more_button").click()
        
        d(text="Rename").click()
        
        original_name = d(resourceId="org.y20k.transistor:id/dialog_rename_station_input").get_text()
        print("original_name: " + original_name)
        new_name = st.text(alphabet=string.ascii_lowercase,min_size=1, max_size=6).example()
        print("new_name: " + new_name)
        d(resourceId="org.y20k.transistor:id/dialog_rename_station_input").set_text(new_name)
        
        d(text="RENAME").click()

        assert d(text=new_name).exists(), "NEW NAME DOES NOT EXIST"
        assert not d(text=original_name).exists(), "OLD NAME STILL EXISTS"
        new_station_count = int(d(resourceId="org.y20k.transistor:id/list_item_textview").count)
        print("new_station_count: " + str(new_station_count))
        assert original_station_count == new_station_count, "station count changed"



t = Test()

setting = Setting(
    apk_path="./apk/transistor/1.2.4.apk",
    device_serial="emulator-5554",
    output_dir="../output/transistor/66/mutate",
    policy_name="mutate",
    number_of_events_that_restart_app = 100
)
start_kea(t,setting)

