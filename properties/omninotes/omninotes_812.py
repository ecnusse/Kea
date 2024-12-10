import sys
sys.path.append("..")
from kea import *

class Test(KeaTest):
    

    @initializer()
    def set_up(self):
        if not d(resourceId="it.feio.android.omninotes:id/fab_expand_menu_button").exists() and d(description="drawer open").exists():
            d(description="drawer open").click()
            
            d(text="Notes").click()
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/done").click()

    @mainPath()
    def rule_restore_backup_shouldnot_change_note_mainpath(self):
        d(resourceId="it.feio.android.omninotes:id/fab_expand_menu_button").click()
        d(text="Text note").click()
        d(resourceId="it.feio.android.omninotes:id/detail_content").set_text("Hello world")
        d(description="drawer open").click()
    
    @precondition(lambda self: d(resourceId="it.feio.android.omninotes:id/menu_search").exists() and d(resourceId="it.feio.android.omninotes:id/note_title").exists() and d(text="Notes").exists() and not d(text="SETTINGS").exists())
    @rule()
    def rule_restore_backup_shouldnot_change_note(self):
        
        
        note_count = int(d(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root").count)
        selected_note = random.randint(0, note_count - 1)
        print("selected_note: " + str(selected_note))
        
        selected_note = d(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root")[selected_note].child(resourceId="it.feio.android.omninotes:id/card_layout")
        
        note_title = selected_note.child(resourceId="it.feio.android.omninotes:id/note_title").get_text()
        print("note_title: " + note_title)
        
        has_content = False
        if selected_note.child(resourceId="it.feio.android.omninotes:id/note_content").exists():
            has_content = True
            note_content = selected_note.child(resourceId="it.feio.android.omninotes:id/note_content").get_text()
            print("note_content: " + note_content)
        
        has_attachment = selected_note.child(resourceId="it.feio.android.omninotes:id/attachmentThumbnail").exists()
        print("has_attachment: " + str(has_attachment))
        
        d(resourceId="it.feio.android.omninotes:id/toolbar").child(className="android.widget.ImageButton").click()
        
        d(text="SETTINGS").click()
        
        d(text="Data").click()
        
        d(text="Sync and Backups").click()
        
        d(text="Backup").click()
        
        back_up_name = d(resourceId="it.feio.android.omninotes:id/export_file_name").get_text()
        d(text="CONFIRM").click()
        
        d(text="Restore or delete backups").click()
        
        d(text=back_up_name).click()
        
        d(text="CONFIRM").click()
        
        d.press("back")
        
        d.press("back")
        
        d.press("back")
        
        d.press("back")
        
        
        assert selected_note.exists(), "selected note not exists"
        if note_title is not None:
            assert selected_note.child(resourceId="it.feio.android.omninotes:id/note_title").get_text() == note_title, "note_title: "  + selected_note.child(resourceId="it.feio.android.omninotes:id/note_title").get_text()
        if has_content:
            assert selected_note.child(resourceId="it.feio.android.omninotes:id/note_content").get_text() == note_content, "note_content: " + selected_note.child(resourceId="it.feio.android.omninotes:id/note_content").get_text()
        assert selected_note.child(resourceId="it.feio.android.omninotes:id/attachmentThumbnail").exists() == has_attachment, "has_attachment: " + str(selected_note.child(resourceId="it.feio.android.omninotes:id/attachmentThumbnail").exists())




if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/omninotes/OmniNotes-6.0.5.apk",
        device_serial="emulator-5554",
        output_dir="../output/omninotes/812/guided",
        policy_name="guided"
    )
    start_kea(t,setting)
    
