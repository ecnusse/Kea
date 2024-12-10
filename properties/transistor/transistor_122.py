import sys
sys.path.append("..")
from kea import *

class Test(KeaTest):
    
    @initializer()
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

    @mainPath()
    def exit_app_and_start_again_shouldnot_change_state_mainpath(self):
        d(resourceId="org.y20k.transistor:id/list_item_textview").click()
        d(resourceId="org.y20k.transistor:id/player_playback_button").click()

    @precondition(
        lambda self: d(text="Now Playing").exists() and 
        d(resourceId="org.y20k.transistor:id/player_textview_station_metadata").exists()
    )
    @rule()
    def exit_app_and_start_again_shouldnot_change_state(self):
        play_text = d(resourceId="org.y20k.transistor:id/player_textview_station_metadata").get_text()
        print("play_text: " + play_text)
        d.press("recent")
        
        d.press("back")
        
        assert d(resourceId="org.y20k.transistor:id/player_textview_station_metadata").get_text() == play_text, "exit app and start again should not change state"




if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/transistor/4.1.7.apk",
        device_serial="emulator-5554",
        output_dir="../output/transistor/122/guided",
        policy_name="guided"
    )
    start_kea(t,setting)
    
