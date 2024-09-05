import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @initialize()
    def set_up(self):
        
        pass

    @precondition(
        lambda self: d(text="Settings").exists() and 
        d(resourceId="de.danoeh.antennapod:id/search").exists() 
    )
    @rule()
    def notification_priority_should_display_in_setting(self):
        text = st.text(alphabet=string.ascii_letters,min_size=1, max_size=4).example()
        d(resourceId="de.danoeh.antennapod:id/search").set_text(text)
        
        if not d(resourceId="de.danoeh.antennapod:id/title").exists():
            print("title not found")
            return
        random_select_title = random.choice(d(resourceId="de.danoeh.antennapod:id/title"))
        title = str(random_select_title.get_text())
        print("random_select_title: " + title)
        
        random_select_title.click()
        
        assert d(text=title).exists(), "title not found "+str(title)


t = Test()

setting = Setting(
    apk_path="./apk/antennapod/1.7.1.apk",
    device_serial="emulator-5554",
    output_dir="output/antennapod/4640/random_100/1",
    policy_name="random",
    
    number_of_events_that_restart_app = 100
)
run_android_check_as_test(t,setting)

