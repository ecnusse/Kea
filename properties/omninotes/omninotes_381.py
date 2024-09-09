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
            
    
    @precondition(lambda self: d(resourceId="it.feio.android.omninotes:id/toolbar").child(text="Trash").exists() and d(resourceId="it.feio.android.omninotes:id/root").exists() and not d(text="SETTINGS").exists())
    @rule()
    def restore_note_from_trash_should_work(self):
        
        note_count = int(d(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root").count)
        selected_note = random.randint(0, note_count - 1)
        print("selected_note: " + str(selected_note))
        
        selected_note = d(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root")[selected_note].child(resourceId="it.feio.android.omninotes:id/card_layout")
        
        note_title = selected_note.child(resourceId="it.feio.android.omninotes:id/note_title").get_text()
        print("note_title: " + note_title)
        note_content = None
        if selected_note.child(resourceId="it.feio.android.omninotes:id/note_content").exists():
            note_content = selected_note.child(resourceId="it.feio.android.omninotes:id/note_content").get_text()
            print("note_content: " + note_content)
        
        is_archive = selected_note.child(resourceId="it.feio.android.omninotes:id/archivedIcon").exists()
        print("is_archive: " + str(is_archive))
        
        selected_note.long_click()
        
        d(resourceId="it.feio.android.omninotes:id/menu_sort").click()
        
        d(resourceId="it.feio.android.omninotes:id/toolbar").child(className="android.widget.ImageButton").click()
        
        if is_archive:
            
            assert d(text="Archive").exists(),"Archive should appear in drawer item"
            
            d(text="Archive").click()
            
            if note_title != "":
                assert d(text=note_title).exists() ,"note should appear in Archive"
            if note_content is not None:
                assert d(text=note_content).exists() ,"note should appear in Archive"
        else:
            d(text="Notes").click()
            
            if note_title != "":
                assert d(text=note_title).exists() ,"note should appear in Notes"
            if note_content is not None:
                assert d(text=note_content).exists() ,"note should appear in Notes"



t = Test()

setting = Setting(
    apk_path="./apk/omninotes/OmniNotes-5.3.2.apk",
    device_serial="emulator-5554",
    output_dir="output/omninotes/381/random_100/1",
    policy_name="random",

    main_path="main_path/omninotes/381.json"
)
run_android_check_as_test(t,setting)
