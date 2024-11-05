from kea.main import *

class Test(Kea):
    

    @initialize()
    def set_up(self):
        d(resourceId="net.gsantner.markor:id/next").click()
        
        d(resourceId="net.gsantner.markor:id/next").click()
        
        d(resourceId="net.gsantner.markor:id/next").click()
        
        d(resourceId="net.gsantner.markor:id/next").click()
        
        d(resourceId="net.gsantner.markor:id/next").click()
        
        d(resourceId="net.gsantner.markor:id/next").click()
        
        d(text="DONE").click()
        
        
        if d(text="OK").exists():
            d(text="OK").click()
        
        
    #bug 600
    @precondition(
        lambda self: d(resourceId="net.gsantner.markor:id/fab_add_new_item").exists() and 
        d(resourceId="net.gsantner.markor:id/action_go_to").exists() and not 
        d(text="Settings").exists() and not d(text="Date").exists() and not 
        d(resourceId="net.gsantner.markor:id/action_rename_selected_item").exists()
        )
    @rule()
    def markor_title_disappear(self):
        assert not d(resourceId="net.gsantner.markor:id/action_go_to").left(className="android.widget.TextView") is None



t = Test()

setting = Setting(
    apk_path="./apk/markor/1.8.3.apk",
    device_serial="emulator-5554",
    output_dir="../output/markor/600/mutate",
    policy_name="mutate"
)
run_android_check_as_test(t,setting)

