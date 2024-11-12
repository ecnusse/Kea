import sys
sys.path.append("..")
from kea.main import *

class Test(Kea):
    
    @mainPath()
    def change_setting_should_not_influence_Download_function_mainpath(self):
        d.press("back")
        d(resourceId="de.danoeh.antennapod:id/discovery_cover").click()
        d(text="SUBSCRIBE").click()
        d(resourceId="de.danoeh.antennapod:id/txtvItemname").click()

    @precondition(
        lambda self: d(text="Download").exists() and d(text="Stream").exists() and d(className="android.webkit.WebView").exists()
    )
    @rule()
    def change_setting_should_not_influence_Download_function(self):
        d(text="Download").click()
        
        assert d(text="Delete").exists() or d(text="Cancel").exists()



if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/antennapod/1.8.0.apk",
        device_serial="emulator-5554",
        output_dir="../output/antennapod/3786/mutate",
        policy_name="mutate"
    )
    start_kea(t,setting)
    
