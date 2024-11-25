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
    def restore_note_from_trash_should_work_mainpath(self):
        d(resourceId="it.feio.android.omninotes:id/fab_expand_menu_button").long_click()
        d(resourceId="it.feio.android.omninotes:id/detail_content").set_text("Hello world")
        d(description="drawer open").click()
        d(resourceId="it.feio.android.omninotes:id/note_title").long_click()
        d(description="More options").click()
        d(text="Trash").click()
        d(description="drawer open").click()
        d(text="Trash").click()

    # bug #381
    @precondition(lambda self: d(resourceId="it.feio.android.omninotes:id/toolbar").child(text="Trash").exists() and d(resourceId="it.feio.android.omninotes:id/root").exists() and not d(text="Settings").exists())
    @rule()
    def restore_note_from_trash_should_work(self):
        
        note_count = int(d(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root").count)
        selected_note = random.randint(0, note_count - 1)
        print("selected_note: " + str(selected_note))
        
        selected_note = d(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root")[selected_note].child(resourceId="it.feio.android.omninotes:id/card_layout")
        
        note_title = selected_note.child(resourceId="it.feio.android.omninotes:id/note_title").get_text()
        print("note_title: " + note_title)
        
        is_archive = selected_note.child(resourceId="it.feio.android.omninotes:id/archivedIcon").exists()
        print("is_archive: " + str(is_archive))
        
        selected_note.long_click(1)
        
        d(resourceId="it.feio.android.omninotes:id/menu_sort").click()
        
        d(resourceId="it.feio.android.omninotes:id/toolbar").child(className="android.widget.ImageButton").click()
        
        if is_archive:
            assert d(text="Archive").exists(),"Archive should appear in drawer item"
            
            d(text="Archive").click()
            assert d(resourceId="it.feio.android.omninotes:id/list").child_by_text(note_title,allow_scroll_search=True).exists(),"note should appear in Archive"
        else:
            d(text="Notes").click()
            
            assert d(resourceId="it.feio.android.omninotes:id/list").child_by_text(note_title,allow_scroll_search=True).exists(),"note should appear in Notes"
    

if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/omninotes/OmniNotes-6.3.1.apk",
        device_serial="emulator-5554",
        output_dir="../output/omninotes/381/mutate_new",
        policy_name="mutate",
        timeout=86400,
        number_of_events_that_restart_app = 100
    )
    start_kea(t,setting)
    
