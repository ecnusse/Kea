import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @precondition(
        lambda self: d(text="Add new station").exists() and 
        d(className="android.widget.EditText").get_text() != "Paste a valid streaming URL"     
    )
    @rule()
    def should_add_station(self):
        print(d(className="android.widget.EditText").get_text())
        d(text="ADD").click()
        time.sleep(3)
        if d(text="Download Issue").exists():
            print("Download Issue")
            return
        assert d(resourceId="org.y20k.transistor:id/list_item_textview").exists() 



t = Test()

setting = Setting(
    apk_path="./apk/transistor/1.1.4.apk",
    device_serial="emulator-5554",
    output_dir="output/transistor/9/random_100/1",
    policy_name="random",
    
    number_of_events_that_restart_app = 100
)
start_kea(t,setting)

