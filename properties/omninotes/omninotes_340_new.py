import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @initialize()
    def set_up(self):
        if d(text="OK").exists():
            d(text="OK").click()
            
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/done").click()
        
        if d(text="OK").exists():
            d(text="OK").click()
             

    # bug #340
    @precondition(lambda self: d(resourceId="it.feio.android.omninotes:id/count").exists() and d(text="Settings").exists())
    @rule()
    def delete_category_should_remove_immediately(self):
        
        category_count = d(resourceId="it.feio.android.omninotes:id/count").count
        selected_category_index = random.randint(0, category_count - 1)
        selected_category = d(resourceId="it.feio.android.omninotes:id/count")[selected_category_index].left(resourceId="it.feio.android.omninotes:id/title")
        selected_category_name = selected_category.get_text()
        print("selected_category_name: " + selected_category_name)
        
        selected_category.long_click()
        
        d(text="DELETE").click()
        
        d(text="CONFIRM").click()
        
        assert not d(text=selected_category_name).exists()
    


t = Test()

setting = Setting(
    apk_path="./apk/omninotes/OmniNotes-6.3.1.apk",
    device_serial="emulator-5554",
    output_dir="output/omninotes/340/mutate_new/1",
    policy_name="random",

    main_path="main_path/omninotes/340_new.json"
)
start_kea(t,setting)

