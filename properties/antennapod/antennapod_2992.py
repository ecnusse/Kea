import sys
sys.path.append("..")
from kea.main import *

class Test(Kea):
    
    @initializer()
    def set_up(self):
        d.press("back")

    @mainPath()
    def rotate_device_shouldnot_make_cover_disappear_mainpath(self):
        d(description="Open menu").click()
        d(text="Add Podcast").click()
        d(text="SEARCH ITUNES").click()
        d(resourceId="de.danoeh.antennapod:id/imgvCover").click()
        d(text="SUBSCRIBE").click()
        d(text="OPEN PODCAST").click()
        d(resourceId="de.danoeh.antennapod:id/txtvItemname").click()
        d(resourceId="de.danoeh.antennapod:id/butAction2").click()

    @precondition(
        lambda self: d(resourceId="de.danoeh.antennapod:id/imgvCover").exists() and d(resourceId="de.danoeh.antennapod:id/audio_controls").exists()
    )
    @rule()
    def rotate_device_shouldnot_make_cover_disappear(self):
        d.set_orientation('l')
        
        d.set_orientation('n')
        
        assert d(resourceId="de.danoeh.antennapod:id/imgvCover").exists()



t = Test()

setting = Setting(
    apk_path="./apk/antennapod/1.7.1.apk",
    device_serial="emulator-5554",
    output_dir="../output/antennapod/2992/mutate",
    policy_name="mutate"
)
start_kea(t,setting)

