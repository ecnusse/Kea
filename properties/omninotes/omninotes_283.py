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
            
        
    
    @precondition(lambda self: d(resourceId="it.feio.android.omninotes:id/search_query").exists() and d(resourceId="it.feio.android.omninotes:id/root").exists() and not d(text="SETTINGS").exists())
    @rule()
    def search_result_should_not_contain_other_notes(self):
        
        text = d(resourceId="it.feio.android.omninotes:id/search_query").get_text().split(" ")[1]
        print("search text: " + text)
        if not d(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root").exists():
            return
        note_count = int(d(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root").count)
        selected_note_number = random.randint(0, note_count - 1)
        selected_note = d(resourceId="it.feio.android.omninotes:id/root")[selected_note_number]
        print("selected_note: " + str(selected_note_number))
        selected_note.click()
        title = d(resourceId="it.feio.android.omninotes:id/detail_title").get_text()
        print("title: " + title)
        content = d(resourceId="it.feio.android.omninotes:id/detail_content").get_text()
        print("content: " + content)
        assert text.lower() in title.lower() or text in content.lower()
    


t = Test()

setting = Setting(
    apk_path="./apk/omninotes/OmniNotes-5.2.15.apk",
    device_serial="emulator-5554",
    output_dir="output/omninotes/283/mutate/1",
    policy_name="random",

    main_path="main_path/omninotes/283.json"
)
start_kea(t,setting)

