from kea.main import *

class Test(Kea):
    

    @initialize()
    def set_up(self):
        d(resourceId="net.gsantner.markor:id/next").click()
        
        d(resourceId="net.gsantner.markor:id/next").click()
        
        d(resourceId="net.gsantner.markor:id/next").click()
        
        d(resourceId="net.gsantner.markor:id/next").click()
        
        d(resourceId="net.gsantner.markor:id/next").click()
        
        d(text="DONE").click()
        
        
        if d(text="OK").exists():
            d(text="OK").click()

    @main_path()
    def change_file_format_should_work_mainpath(self):
        d(resourceId="net.gsantner.markor:id/fab_add_new_item").click()
        d(resourceId="net.gsantner.markor:id/new_file_dialog__name").set_text("Hello")
        d(text="OK").click()
        d(resourceId="net.gsantner.markor:id/document__fragment__edit__content_editor__scrolling_parent").set_text("World")
        d(resourceId="net.gsantner.markor:id/action_preview").click()

    
    @precondition(
        lambda self: d(resourceId="net.gsantner.markor:id/action_edit").exists() and
          d(className="android.webkit.WebView").child(className="android.view.View").exists() and not
          d(text="todo").exists()
        )
    @rule()
    def format_should_retain_next_time_open_it(self):
        content = d(className="android.webkit.WebView").child(className="android.view.View").get_text()
        print("content: "+str(content))
        title = d(resourceId="net.gsantner.markor:id/note__activity__text_note_title").get_text()
        print("title: "+str(title))
        d.press("back")
        
        if d(resourceId="net.gsantner.markor:id/action_edit").exists():
            d.press("back")
            
        d(textStartsWith=title).click()
        
        if d(resourceId="net.gsantner.markor:id/action_preview").exists():
            d(resourceId="net.gsantner.markor:id/action_preview").click()
            
        content2 = d(className="android.webkit.WebView").child(className="android.view.View").get_text()
        print("content2: "+str(content2))
        assert content == content2



t = Test()

setting = Setting(
    apk_path="./apk/markor/2.5.0.apk",
    device_serial="emulator-5554",
    output_dir="../output/markor/1220/mutate",
    policy_name="mutate"
)
run_android_check_as_test(t,setting)

