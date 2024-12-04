import sys
sys.path.append("..")
from kea.core import *

class Test(Kea):
    

    @initializer()
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

    @mainPath()
    def delete_category_should_remove_immediately_mainpath(self):
        d(resourceId="it.feio.android.omninotes:id/fab_expand_menu_button").long_click()
        d(resourceId="it.feio.android.omninotes:id/detail_title").set_text("Hello World")
        d(resourceId="it.feio.android.omninotes:id/menu_category").click()
        d(text="ADD CATEGORY").click()
        d(resourceId="it.feio.android.omninotes:id/category_title").set_text("Hello")
        d(resourceId="it.feio.android.omninotes:id/save").click()
        d.press("back")
        d.press("back")
        d(description="drawer open").click()

    # bug #340
    @precondition(lambda self: d(resourceId="it.feio.android.omninotes:id/count").exists() and d(text="Settings").exists())
    @rule()
    def delete_category_should_remove_immediately(self):
        
        category_count = d(resourceId="it.feio.android.omninotes:id/count").count
        selected_category_index = random.randint(0, category_count - 1)
        selected_category = d(resourceId="it.feio.android.omninotes:id/count")[selected_category_index].left(resourceId="it.feio.android.omninotes:id/title")
        selected_category_name = selected_category.get_text()
        print("selected_category_name: " + selected_category_name)
        
        selected_category.long_click(1)
        
        d(text="DELETE").click()
        
        d(text="CONFIRM").click()
        
        assert not d(text=selected_category_name).exists()
    


if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/omninotes/OmniNotes-6.3.1.apk",
        device_serial="emulator-5554",
        output_dir="../output/omninotes/340/guided_new",
        policy_name="guided"
    )
    start_kea(t,setting)
    
