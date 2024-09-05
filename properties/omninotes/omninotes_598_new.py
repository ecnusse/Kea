import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):

    @initialize()
    def set_up(self):
        d.set_fastinput_ime(True)
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/done").click()
        
        if d(text="OK").exists():
            d(text="OK").click()
            
        
        d(description="drawer open").click()
        
        d(text="Settings").click()
        
        d(text="Navigation").click()
        
        d(text="Group not categorized").click()
        
        d(description="Navigate up").click()
        
        d(description="Navigate up").click()
        
        d.press("back")
        
        
        d(resourceId="it.feio.android.omninotes:id/fab_expand_menu_button").click()
        
        d(text="Text note").click()
        
        d(resourceId="it.feio.android.omninotes:id/detail_title").set_text("test")
        
        d(resourceId="it.feio.android.omninotes:id/detail_content").set_text("#bb")
        
        
        d(resourceId="it.feio.android.omninotes:id/menu_category").click()
        
        d(text="ADD CATEGORY").click()
        
        category_name = st.text(alphabet=string.printable,min_size=1, max_size=10).example()
        d(resourceId="it.feio.android.omninotes:id/category_title").set_text(category_name)
        
        d(text="OK").click()
        
        # lock note
        d(description="More options").click()
        
        d(text="Lock").click()
        
        d(resourceId="it.feio.android.omninotes:id/password").set_text("1")
        
        d(resourceId="it.feio.android.omninotes:id/password_check").set_text("1")
        
        d(resourceId="it.feio.android.omninotes:id/question").set_text("1")
        
        d(resourceId="it.feio.android.omninotes:id/answer").set_text("1")
        
        d(resourceId="it.feio.android.omninotes:id/answer_check").set_text("1")
        
        d(scrollable=True).fling()
        
        d(text="OK").click()
        time.sleep(2)
        d.press("back")
        
    
    @precondition(lambda self: d(text="Data").exists() and d(text="Password").exists())
    @rule()
    def remove_password_in_setting_should_effect(self):
        
        d(text="Password").click()
        
        d(text="REMOVE PASSWORD").click()
        
        d(resourceId="it.feio.android.omninotes:id/password_request").set_text("1")
        
        d(text="OK").click()
        
        d(text="OK").click()
        
        d.press("back")
        
        d.press("back")
        
        d.press("back")
        
        d.press("back")
        # open note
        if not d(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root").exists():
            print("no note")
            return
        note_count = int(d(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root").count)
        selected_note = random.randint(0, note_count - 1)
        print("selected_note: " + str(selected_note))
        
        d(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root")[selected_note].click()
        
        assert not d(text="PASSWORD FORGOTTEN").exists()
    
    @precondition(lambda self: d(description="More options").exists() and d(resourceId="it.feio.android.omninotes:id/menu_attachment").exists())
    @rule()
    def action_lock_a_note(self):
        title = st.text(alphabet=string.printable,min_size=1, max_size=10).example()
        print("title: " + title)
        d(resourceId="it.feio.android.omninotes:id/detail_title").set_text(title)
        
        d(description="More options").click()
        
        d(text="Lock").click()
        
        if d(text="Insert password").exists():
            d(resourceId="it.feio.android.omninotes:id/password_request").set_text("1")
            
            d(text="OK").click()
            time.sleep(3)
            d.press("back")
        else:
            d(resourceId="it.feio.android.omninotes:id/password").set_text("1")
            
            d(resourceId="it.feio.android.omninotes:id/password_check").set_text("1")
            
            d(resourceId="it.feio.android.omninotes:id/question").set_text("1")
            
            d(resourceId="it.feio.android.omninotes:id/answer").set_text("1")
            
            d(resourceId="it.feio.android.omninotes:id/answer_check").set_text("1")
            
            d(scrollable=True).fling()
            
            d(text="OK").click()
            time.sleep(3)
            d.press("back")



t = Test()

setting = Setting(
    apk_path="./apk/omninotes/OmniNotes-6.3.0.apk",
    device_serial="emulator-5554",
    output_dir="output/omninotes/598/1",
    policy_name="random",
    
    number_of_events_that_restart_app = 100
)
run_android_check_as_test(t,setting)

