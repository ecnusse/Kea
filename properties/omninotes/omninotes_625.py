import string
import sys
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @initializer()
    def set_up(self):
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/done").click()
        
    @mainPath()
    def rule_add_category_should_change_number_mainpath(self):
        d(resourceId="it.feio.android.omninotes:id/fab_expand_menu_button").long_click()
        d(resourceId="it.feio.android.omninotes:id/menu_category").click()
    
    @precondition(lambda self: d(text="Categorize as").exists())
    @rule()
    def rule_add_category_should_change_number(self):
        
        d(text="ADD CATEGORY").click()
        
        category_name = st.text(alphabet=string.printable,min_size=1, max_size=10).example()
        d(resourceId="it.feio.android.omninotes:id/category_title").set_text(category_name)
        
        d(text="OK").click()
        
        d(resourceId="it.feio.android.omninotes:id/menu_category").click()
        
        print("category_name: " + category_name)
        
        #assert d(resourceId="it.feio.android.omninotes.alpha:id/md_contentRecyclerView").child_by_text(category_name,allow_scroll_search=True).exists()
        if not d(text=category_name).exists():
            if d(scrollable=True).exists():
                print("scroll to category_name: " + category_name)
                d(scrollable=True).scroll.to(text=category_name)
        assert d(text=category_name).exists(), "category_name: " + category_name
        # assert d(text=category_name).exists(), "category_name: " + category_name
        
        assert d(text=category_name).right(resourceId="it.feio.android.omninotes:id/count").get_text() == "1", "category_name: " + category_name
    



t = Test()

setting = Setting(
    apk_path="./apk/omninotes/OmniNotes-5.4.0.apk",
    device_serial="emulator-5554",
    output_dir="../output/omninotes/625/mutate",
    policy_name="mutate"
)
start_kea(t,setting)

