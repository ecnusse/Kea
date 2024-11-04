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
        lambda self: d(text="Now Playing").exists() and not d(text="Delete").exists()
    )
    @rule()
    def back_button_should_return_to_the_main_list(self):
        d.press("back") 
        
        assert d(text="Transistor").exists(), "back button does not return to the main list"



t = Test()

setting = Setting(
    apk_path="./apk/transistor/2.1.5.apk",
    device_serial="emulator-5554",
    output_dir="../output/transistor/107/mutate",
    policy_name="mutate",
    
    number_of_events_that_restart_app = 100
)
run_android_check_as_test(t,setting)

