import sys
sys.path.append("..")
from kea.core import *

class Test(Kea):

    @initializer()
    def set_up(self):
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/done").click()
        
        
        d(description="drawer open").click()
        
        d(text="Settings").click()
        
        d(text="Navigation").click()
        
        d(text="Group not categorized").click()
        
        d(description="Navigate up").click()
        
        d(description="Navigate up").click()
        
        d.press("back")

    @mainPath()
    def rule_uncategory_should_contain_notes_mainpath(self):
        d(resourceId="it.feio.android.omninotes:id/fab_expand_menu_button").long_click()
        d(resourceId="it.feio.android.omninotes:id/detail_content").set_text("Hello world")
        d.press("back")
        d.press("back")
        d(description="drawer open").click()
    
    # bug #401
    @precondition(lambda self: d(text="Uncategorized").exists() and d(text="Settings").exists())
    @rule()
    def rule_uncategory_should_contain_notes(self):
        d(text="Uncategorized",resourceId="it.feio.android.omninotes:id/title").click()
        
        assert d(resourceId="it.feio.android.omninotes:id/root").exists()
   



if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/omninotes/OmniNotes-6.2.8.apk",
        device_serial="emulator-5554",
        output_dir="../output/omninotes/401/guided_new",
        policy_name="guided",
        # run_initial_rules_after_every_mutation=False
    )
    start_kea(t,setting)
    
