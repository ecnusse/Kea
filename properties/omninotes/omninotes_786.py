import sys
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

    @main_path()
    def rule_remove_tag_from_note_shouldnot_affect_content_mainpath(self):
        d(resourceId="it.feio.android.omninotes:id/fab_expand_menu_button").long_click()
        d(resourceId="it.feio.android.omninotes:id/detail_content").set_text("#hello")
    
    @precondition(lambda self: d(resourceId="it.feio.android.omninotes:id/menu_attachment").exists() and d(resourceId="it.feio.android.omninotes:id/menu_share").exists() and d(resourceId="it.feio.android.omninotes:id/menu_tag").exists() )
    @rule()
    def rule_remove_tag_from_note_shouldnot_affect_content(self):
        
        d(description = "More options").click()
        
        if d(text="Disable checklist").exists():
            d(text="Disable checklist").click()
        else:
            d.press("back")
        origin_content = d(resourceId="it.feio.android.omninotes:id/detail_content").info["text"]
        print("origin_content: " + str(origin_content))
        
        d(resourceId="it.feio.android.omninotes:id/menu_tag").click()
        
        if not d(className="android.widget.CheckBox").exists():
            print("no tag in tag list")
            return
        tag_list_count = int(d(className="android.widget.CheckBox").count)
        #tag_list_count = int(d(resourceId="it.feio.android.omninotes:id/md_control").count)
        tagged_notes = []
        for i in range(tag_list_count):
            # if d(resourceId="it.feio.android.omninotes:id/md_control")[i].info["checked"]:
            if d(className="android.widget.CheckBox")[i].info["checked"]:
                tagged_notes.append(i)
        if len(tagged_notes) == 0:
            print("no tag selected in tag list, random select one")
            selected_note_number = random.randint(0, tag_list_count - 1)
            d(className="android.widget.CheckBox")[selected_note_number].click()
            
            return
        selected_tag_number = random.choice(tagged_notes)
        select_tag_box = d(resourceId="it.feio.android.omninotes:id/control")[selected_tag_number]
        select_tag_name = d(resourceId="it.feio.android.omninotes:id/title")[selected_tag_number+1].info["text"].split(" ")[0]
        print("selected_tag_number: " + str(selected_tag_number))
        print("selected_tag_name: " + str(select_tag_name))
        select_tag_name = "#"+select_tag_name
        
        select_tag_box.click()
        
        d(text="OK").click()
        

        assert not d(textContains=select_tag_name).exists(), "tag should be removed from note" 
        new_content = d(resourceId="it.feio.android.omninotes:id/detail_content").info["text"].strip()
        print("new_content: " + str(new_content))
        origin_content_exlude_tag = origin_content.replace(select_tag_name, "").strip()
        print("origin_content_exlude_tag: " + str(origin_content_exlude_tag))
        
        assert new_content == origin_content_exlude_tag, "content should not be affected by removing tag"
    


t = Test()

setting = Setting(
    apk_path="./apk/omninotes/OmniNotes-6.0.5.apk",
    device_serial="emulator-5554",
    output_dir="../output/omninotes/786/mutate",
    policy_name="mutate",
    
    number_of_events_that_restart_app = 100
)
start_kea(t,setting)

