import sys
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @initializer()
    def set_up(self):
        if d(text="OK").exists():
            d(text="OK").click()

    @mainPath()
    def task_prefilled_when_filtered_mainapth(self):
        d(resourceId="nl.mpcjanssen.simpletask:id/fab").click()
        d(resourceId="nl.mpcjanssen.simpletask:id/taskText").set_text("Hello World!")
        d(resourceId="nl.mpcjanssen.simpletask:id/btnSave").click()

    @precondition(
        lambda self: int(d(resourceId="nl.mpcjanssen.simpletask:id/tasktext").count) > 0 and not d(resourceId="nl.mpcjanssen.simpletask:id/filter_text").exists() and not d(text="Quick filter").exists() and not d(text="Settings").exists() and not d(text="Saved filters").exists()
    )
    @rule()
    def task_prefilled_when_filtered(self):
        d(resourceId="nl.mpcjanssen.simpletask:id/filter").click()
        

        if random.randint(0, 1) == 0:
            d(text="LIST").click()
        else:
            d(text="TAG").click()
        

        invert_filter = random.randint(0, 1) == 0
        if invert_filter:
            d(resourceId="nl.mpcjanssen.simpletask:id/checkbox").click()
        filter_count = int(d(resourceId="android:id/text1").count)
        print("filter count: "+str(filter_count))
        selected_filter_index = random.randint(0, filter_count - 1)
        selected_filer_name = d(resourceId="android:id/text1")[selected_filter_index].get_text()
        print("selected filter: "+str(selected_filer_name))
        d(resourceId="android:id/text1")[selected_filter_index].click()
        
        d(resourceId="nl.mpcjanssen.simpletask:id/menu_filter_action").click()
        
        assert d(resourceId="nl.mpcjanssen.simpletask:id/filter_text").exists(), "filter text should exist"
        
        d(resourceId="nl.mpcjanssen.simpletask:id/fab").click()
        
        content = str(d(resourceId="nl.mpcjanssen.simpletask:id/taskText").get_text())
        print("content: "+str(content))
        if selected_filer_name == "-":
            assert content == "None", "task text should be empty"
        else:
            print("content: "+str(content))
            if invert_filter:
                assert selected_filer_name not in content, "selected_filer_name should not be in content"
            else:
                assert selected_filer_name in content, "selected_filer_name should be in content"
        


if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/simpletask/11.0.1.apk",
        device_serial="emulator-5554",
        output_dir="../output/simpletask/mutate_new",
        policy_name="mutate",
    
    )
    start_kea(t,setting)
    
