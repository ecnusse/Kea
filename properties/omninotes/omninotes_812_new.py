import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @initialize()
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
        
        d(text="Settings").click()
        
        d(text="Data").click()
        
        d(text="Sync and Backups").click()
        
        d(text="Backup").click()
        
        if d(textContains="ALLOW ACCESS TO").exists():
            d(textContains="ALLOW ACCESS TO").click()
            
            if d(text="ALLOW").exists():
                d(text="ALLOW").click()
            if d(text="Allow").exists():
                d(text="Allow").click()
            
        back_up_name = d(resourceId="it.feio.android.omninotes:id/export_file_name").get_text()
        d(text="CONFIRM").click()
        
        d(text="Restore or delete backups").click()
        
        d(text=back_up_name).click()
        
        d(text="RESTORE").click()
        
        d(text="CONFIRM").click()
        
        d.press("back")
        
        d.press("back")
        
        d.press("back")
        
        d.press("back")
        
        # 检查note的title，content，是否有attachment是否发生了变化
        assert selected_note.exists(), "selected note not exists"
        if note_title is not None:
            assert selected_note.child(resourceId="it.feio.android.omninotes:id/note_title").get_text() == note_title, "note_title: "  + selected_note.child(resourceId="it.feio.android.omninotes:id/note_title").get_text()
        if has_content:
            assert selected_note.child(resourceId="it.feio.android.omninotes:id/note_content").get_text() == note_content, "note_content: " + selected_note.child(resourceId="it.feio.android.omninotes:id/note_content").get_text()
        assert selected_note.child(resourceId="it.feio.android.omninotes:id/attachmentThumbnail").exists() == has_attachment, "has_attachment: " + str(selected_note.child(resourceId="it.feio.android.omninotes:id/attachmentThumbnail").exists())




t = Test()

setting = Setting(
    apk_path="./apk/omninotes/OmniNotes-6.3.1.apk",
    device_serial="emulator-5554",
    output_dir="output/omninotes/812/1",
    policy_name="random",

    main_path="main_path/omninotes/812_new.json"
)
run_android_check_as_test(t,setting)

