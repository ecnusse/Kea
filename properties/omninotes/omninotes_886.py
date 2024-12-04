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
        
    @mainPath()
    def rule_trash_note_cannot_be_searched_mainapth(self):
        d(resourceId="it.feio.android.omninotes:id/fab_expand_menu_button").click()
        d(text="Text note").click()
        d(resourceId="it.feio.android.omninotes:id/detail_content").set_text("Hello world")
        d(description="drawer open").click()
        d(resourceId="it.feio.android.omninotes:id/note_title").long_click()
        d(description="More options").click()
        d(text="Trash").click()
        d(description="drawer open").click()
        d(text="Trash").click()
    
    @precondition(lambda self: d(resourceId="it.feio.android.omninotes:id/note_title").exists() and d(text="Trash").exists() and not d(text="Settings").exists())
    @rule()
    def rule_trash_note_cannot_be_searched(self):
        note_count = int(d(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root").count)
        selected_note = random.randint(0, note_count - 1)
        selected_note_name = d(resourceId="it.feio.android.omninotes:id/note_title")[selected_note].info['text']
        print("selected_note_title: " + selected_note_name)
        selected_note_content = d(resourceId="it.feio.android.omninotes:id/note_title")[selected_note].sibling(resourceId="it.feio.android.omninotes:id/note_content")
        
        has_content = False
        if selected_note_content.exists():
            selected_note_content = selected_note_content.get_text()
            print("selected_note_content: " + selected_note_content)
            has_content = True
        
        print("selected_note: " + str(selected_note))
        
        d(resourceId="it.feio.android.omninotes:id/toolbar").child(className="android.widget.ImageButton").click()
        
        d(text="Notes").click()
        
        
        d(resourceId="it.feio.android.omninotes:id/menu_search").click()
        
        d(resourceId="it.feio.android.omninotes:id/search_src_text").set_text(selected_note_name)
        
        d.send_action("search")
        
        if has_content:
            assert not (d(text=selected_note_content,resourceId="it.feio.android.omninotes:id/note_content").exists() and d(text=selected_note_content,resourceId="it.feio.android.omninotes:id/note_content").sibling(resourceId="it.feio.android.omninotes:id/note_title").get_text() == selected_note_name), "selected_note_content: " + selected_note_content
        else:
            assert not (d(text=selected_note_name,resourceId="it.feio.android.omninotes:id/note_title").exists() and not d(text=selected_note_name,resourceId="it.feio.android.omninotes:id/note_title").sibling(resourceId="it.feio.android.omninotes:id/note_content").exists()), "selected_note_name: " + selected_note_name
        print("check list")
        
        d(resourceId="it.feio.android.omninotes:id/menu_uncomplete_checklists").click()
        
        if has_content:
            assert not (d(text=selected_note_content,resourceId="it.feio.android.omninotes:id/note_content").exists() and d(text=selected_note_content,resourceId="it.feio.android.omninotes:id/note_content").sibling(resourceId="it.feio.android.omninotes:id/note_title").get_text() == selected_note_name), "selected_note_content: " + selected_note_content
        else:
            assert not (d(text=selected_note_name,resourceId="it.feio.android.omninotes:id/note_title").exists() and not d(text=selected_note_name,resourceId="it.feio.android.omninotes:id/note_title").sibling(resourceId="it.feio.android.omninotes:id/note_content").exists()), "selected_note_name: " + selected_note_name
   


if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/omninotes/OmniNotes-6.1.0.apk",
        device_serial="emulator-5554",
        output_dir="../output/omninotes/886/guided",
        policy_name="guided"
    )
    start_kea(t,setting)
    
