import string
from kea.main import *

class Test(Kea):
    

    @initialize()
    def set_up(self):
        d(resourceId="net.gsantner.markor:id/next").click()
        
        d(resourceId="net.gsantner.markor:id/next").click()
        
        d(resourceId="net.gsantner.markor:id/next").click()
        
        d(resourceId="net.gsantner.markor:id/next").click()
        
        d(text="DONE").click()
        
        
        if d(text="OK").exists():
            d(text="OK").click()
        
    
    # bug #389
    @precondition(lambda self: d(resourceId="net.gsantner.markor:id/fab_add_new_item").exists() and 
                  d(resourceId="net.gsantner.markor:id/opoc_filesystem_item__title").count < 4)
    @rule()
    def create_file_should_only_create_one(self):
        hidenfile = d(text=".app").exists()
        file_count = int(d(resourceId="net.gsantner.markor:id/opoc_filesystem_item__title").count)
        print("file_count: " + str(file_count))
        d(resourceId="net.gsantner.markor:id/fab_add_new_item").click()
        
        title = st.text(alphabet=string.ascii_lowercase,min_size=1, max_size=6).example()
        d(resourceId="net.gsantner.markor:id/new_file_dialog__name").set_text(title)
        
        d(text="OK").click()
        
        content = st.text(alphabet=string.ascii_lowercase,min_size=5, max_size=6).example()
        print("content: " + str(content))
        d(className="android.widget.EditText").set_text(content)
        
        d.press("back")
        
        if d(resourceId="net.gsantner.markor:id/action_preview").exists():
            d.press("back")
        
        hidenfile_new = d(text=".app").exists()
        if not hidenfile and hidenfile_new:
            return
        new_count = int(d(resourceId="net.gsantner.markor:id/opoc_filesystem_item__title").count)
        print("new_count: " + str(new_count))
        assert new_count == file_count + 1
        



t = Test()

setting = Setting(
    apk_path="./apk/markor/2.11.1.apk",
    device_serial="emulator-5554",
    output_dir="../output/markor/389/mutate_new",
    policy_name="mutate"
)
run_android_check_as_test(t,setting)

