import sys
sys.path.append("..")
from kea.main import *

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
    def remove_password_should_not_affect_notes_MAINPATH(self):
        d(resourceId="it.feio.android.omninotes:id/fab_expand_menu_button").long_click()
        d(resourceId="it.feio.android.omninotes:id/detail_title").set_text("Hello")

    @precondition(lambda self: d(resourceId="it.feio.android.omninotes:id/menu_attachment").exists() and d(resourceId="it.feio.android.omninotes:id/detail_title").get_text() != "Title")
    @rule()
    def remove_password_should_not_affect_notes(self):
        
        note_title = d(resourceId="it.feio.android.omninotes:id/detail_title").get_text()
        print("title: " + str(note_title))
        
        content = d(resourceId="it.feio.android.omninotes:id/detail_content").get_text()
        print("content: " + str(content))
        
        d(description="More options").click()
        
        if d(text="Lock").exists():
            d(text="Lock").click()
            
            if d(resourceId="it.feio.android.omninotes:id/password_request").exists():
                d(resourceId="it.feio.android.omninotes:id/password_request").set_text("1")
                
                d(text="OK").click()
            else:    
                d(resourceId="it.feio.android.omninotes:id/password").set_text("1")
                
                d(resourceId="it.feio.android.omninotes:id/password_check").set_text("1")
                
                d(resourceId="it.feio.android.omninotes:id/question").set_text("1")
                
                d(resourceId="it.feio.android.omninotes:id/answer").set_text("1")
                
                d(resourceId="it.feio.android.omninotes:id/answer_check").set_text("1")
                
                d(scrollable=True).fling()
                
                d(text="OK").click()
                time.sleep(2)
                d.press("back")
            
        else:
            print("the note has been lock, return")
            d(text="Unlock").click()
            return
        time.sleep(2)
        d.press("back")

        
        d(resourceId="it.feio.android.omninotes:id/toolbar").child(className="android.widget.ImageButton").click()
        
        d(text="Settings").click()
        
        d(text="Data").click()
        
        d(text="Password").click()
        
        d(text="REMOVE PASSWORD").click()
        
        if not d(text="Insert password").exists():
            print("password is not set, return")
            return 
        d(resourceId="it.feio.android.omninotes:id/password_request").set_text("1")
        
        d(text="OK").click()
        
        d(text="OK").click()
        time.sleep(2)
        d.press("back")
        
        d.press("back")
        
        d.press("back")
        
        assert d(text=note_title).exists()," note title should exists the same as before "+str(note_title)
        d(text=note_title).click()
        
        assert str(d(resourceId="it.feio.android.omninotes:id/detail_content").get_text()) == content," note content should exists the same as before "+str(content)
        d.press("back")



t = Test()

setting = Setting(
    apk_path="./apk/omninotes/OmniNotes-6.3.0.apk",
    device_serial="emulator-5554",
    output_dir="../output/omninotes/104/mutate_new",
    policy_name="mutate",
    timeout=86400,
    number_of_events_that_restart_app = 100
)
start_kea(t,setting)

