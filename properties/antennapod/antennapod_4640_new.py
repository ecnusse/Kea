import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    


    @precondition(
        lambda self: d(text="Settings").exists() and 
        d(text="Search…").exists() 
    )
    @rule()
    def notification_priority_should_display_in_setting(self):
        texts = st.text(alphabet=string.ascii_letters,min_size=1, max_size=4).example()
        print("text: " + texts)
        d(text="Search…").set_text(texts)
        
        if not d(resourceId="android:id/title").exists():
            print("title not found")
            return
        random_select_title = random.choice(d(resourceId="android:id/title"))
        title = str(random_select_title.get_text())
        print("random_select_title: " + title)
        
        random_select_title.click()
        
        assert d(text=title).exists(), "title not found "+str(title)


t = Test()

setting = Setting(
    apk_path="./apk/antennapod/3.2.0.apk",
    device_serial="emulator-5554",
    output_dir="output/antennapod/4640/random_100/1",
    policy_name="random",
    
    number_of_events_that_restart_app = 100
)
run_android_check_as_test(t,setting)

