import sys
sys.path.append("..")
from kea import *

class Test(KeaTest):

    @mainPath()
    def rotate_device_shouldnot_make_cover_disappear_mainpath(self):
        d(description="Open menu").click()
        d(text="Add podcast").click()
        d(text="Show suggestions").click()
        d(resourceId="de.danoeh.antennapod:id/discovery_cover").click()
        d(text="Subscribe").click()
        d(resourceId="de.danoeh.antennapod:id/progress").click()
        d(resourceId="de.danoeh.antennapod:id/butAction1").click()
        d(resourceId="de.danoeh.antennapod:id/playerFragment").click()

    @precondition(
        lambda self: d(resourceId="de.danoeh.antennapod:id/imgvCover").exists() and d(resourceId="de.danoeh.antennapod:id/audio_controls").exists()
    )
    @rule()
    def rotate_device_shouldnot_make_cover_disappear(self):
        d.set_orientation('l')
        
        d.set_orientation('n')
        
        assert d(resourceId="de.danoeh.antennapod:id/imgvCover").exists()





if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/antennapod/3.2.0.apk",
        device_serial="emulator-5554",
        output_dir="../output/antennapod/2992/guided_new",
        policy_name="guided",
        timeout=86400,
        number_of_events_that_restart_app = 100
    )
    start_kea(t,setting)
    
