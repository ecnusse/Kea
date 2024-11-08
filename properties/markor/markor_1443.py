from kea.main import *

class Test(Kea):
    

    @initializer()
    def set_up(self):
        d(resourceId="net.gsantner.markor:id/next").click()
        
        d(resourceId="net.gsantner.markor:id/next").click()
        
        d(resourceId="net.gsantner.markor:id/next").click()
        
        d(resourceId="net.gsantner.markor:id/next").click()
        
        d(resourceId="net.gsantner.markor:id/next").click()
        
        d(text="DONE").click()
        
        
        if d(text="OK").exists():
            d(text="OK").click()
        
    @mainPath()
    def setting_should_be_clicked_mainpath(self):
        d(resourceId="net.gsantner.markor:id/nav_more").click()
    
    @precondition(
        lambda self: d(resourceId="net.gsantner.markor:id/nav_more").exists() and
        d(resourceId="net.gsantner.markor:id/nav_more").info["selected"] 
    )
    @rule()
    def setting_should_be_clicked(self):
        d(scrollable=True).fling.vert.backward()
        
        #click setting
        d(resourceId="net.gsantner.markor:id/recycler_view").child(resourceId="android:id/title")[2].click()
        
        assert not d(resourceId="net.gsantner.markor:id/nav_more").exists()




t = Test()

setting = Setting(
    apk_path="./apk/markor/2.8.0.apk",
    device_serial="emulator-5554",
    output_dir="../output/markor/1443/mutate",
    policy_name="mutate"
)
start_kea(t,setting)

