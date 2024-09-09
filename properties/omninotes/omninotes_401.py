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
        
        if d(text="OK").exists():
            d(text="OK").click()
            
        # 打开设置-在navigation 中显示没有被分类的Notes
        d(resourceId="it.feio.android.omninotes:id/fab_expand_menu_button").long_click()
        
        d.press("back")
        time.sleep(2)
        d(resourceId="it.feio.android.omninotes:id/toolbar").child(className="android.widget.ImageButton").click()
        
        if not d(text="SETTINGS").exists():
            d(resourceId="it.feio.android.omninotes:id/toolbar").child(className="android.widget.ImageButton").click()
        d(text="SETTINGS").click()
        
        d(text="Navigation").click()
        
        d(text="Group not categorized").click()
        
        d.press("back")
        
        d.press("back")
        
        d.press("back")
        
    
    @precondition(lambda self: d(text="Uncategorized").exists() and d(text="SETTINGS").exists())
    @rule()
    def rule_uncategory_should_contain_notes(self):
        d(text="Uncategorized",resourceId="it.feio.android.omninotes:id/title").click()
        
        assert d(resourceId="it.feio.android.omninotes:id/root").exists()
        



t = Test()

setting = Setting(
    apk_path="./apk/omninotes/OmniNotes-5.4.0.apk",
    device_serial="emulator-5554",
    output_dir="output/omninotes/401/random_100/1",
    policy_name="random",

    main_path="main_path/omninotes/401.json",
    run_initial_rules_after_every_mutation=False
)
