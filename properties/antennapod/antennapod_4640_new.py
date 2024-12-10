import string
import sys
sys.path.append("..")
from kea import *

class Test(KeaTest):

    @mainPath()
    def text_should_display_when_episodes_is_empty_mainpath(self):
        d(description="Open menu").click()
        d(text="Settings").click()

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


if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/antennapod/3.2.0.apk",
        device_serial="emulator-5554",
        output_dir="../output/antennapod/4640/guided_new",
        policy_name="guided",
        
        number_of_events_that_restart_app = 100
    )
    start_kea(t,setting)
    
