import sys
sys.path.append("..")
from kea.core import *

class Test(Kea):

    @mainPath()
    def rename_dialog_shouldnot_hide_mainpath(self):
        d(resourceId="com.ichi2.anki:id/fab_expand_menu_button").click()
        d(text="Create deck").click()
        d(className="android.widget.EditText").set_text('Custom study session')
        d(text="OK").click()

    @precondition(
        lambda self: d(resourceId="com.ichi2.anki:id/fab_expand_menu_button").exists() and 
        d(text="Custom study session").exists() and 
        d(resourceId="com.ichi2.anki:id/action_sync").exists() and not
        d(text="Card browser").exists() 
    )
    @rule()
    def rename_dialog_shouldnot_hide(self):
        d(text="Custom study session").long_click()
        
        d(text="Custom study").click()
        
        d(text="Review ahead").click()
        
        d(text="OK").click()
        

        assert d(text="Rename the existing custom study deck first").exists(), "rename dialog should not hide"



if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/ankidroid/2.13.5.apk",
        device_serial="emulator-5554",
        output_dir="../output/ankidroid/7680/mutate",
        policy_name="mutate"
    )
    start_kea(t,setting)
    
