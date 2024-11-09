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
    def format_change_should_work_in_view_mode_mainpath(self):
        d(resourceId = "net.gsantner.markor:id/nav_todo").click()
        
    @precondition(
        lambda self: d(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").exists() and 
         d(resourceId="net.gsantner.markor:id/action_preview").exists() and not
         d(text="Settings").exists() and not 
         d(text="Date").exists() and not 
         d(resourceId="net.gsantner.markor:id/action_rename_selected_item").exists()
        )
    @rule()
    def format_change_should_work_in_view_mode(self):
        
        d(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").set_text("# test")
        
        d(resourceId="net.gsantner.markor:id/action_preview").click()
        
        d(description="More options").click()
        
        d(text="Format").click()
        
        d(text="Markdown").click()
        
        assert not "#" in str(d(className="android.webkit.WebView").child(className="android.view.View").info["text"])




t = Test()

setting = Setting(
    apk_path="./apk/markor/2.1.3.apk",
    device_serial="emulator-5554",
    output_dir="../output/markor/703/mutate_new",
    policy_name="mutate"
)
start_kea(t,setting)

