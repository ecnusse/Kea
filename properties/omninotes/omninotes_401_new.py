import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):

    @initialize()
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

    
    # bug #401
    @precondition(lambda self: d(text="Uncategorized").exists() and d(text="Settings").exists())
    @rule()
    def rule_uncategory_should_contain_notes(self):
        d(text="Uncategorized",resourceId="it.feio.android.omninotes:id/title").click()
        
        assert d(resourceId="it.feio.android.omninotes:id/root").exists()
   



t = Test()

setting = Setting(
    apk_path="./apk/omninotes/OmniNotes-6.2.8.apk",
    device_serial="emulator-5554",
    output_dir="output/omninotes/401/mutate_new/1",
    policy_name="random",

    main_path="main_path/omninotes/401_new.json",
    run_initial_rules_after_every_mutation=False
)

