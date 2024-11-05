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
        
    
    @precondition(lambda self: d(resourceId="it.feio.android.omninotes:id/note_title").exists() and d(text="Notes").exists() and not d(text="Settings").exists() and d(resourceId="it.feio.android.omninotes:id/lockedIcon").exists())
    @rule()
    def swipe_locked_note(self):
        
        selected_note = d(resourceId="it.feio.android.omninotes:id/lockedIcon").up(resourceId="it.feio.android.omninotes:id/note_title")
        selected_note_text = selected_note.get_text()
        print("selected_note_text: " + selected_note_text)
        
        selected_note.scroll.horiz.forward(steps=100)
        time.sleep(3)
        d.press("recent")
        
        d.press("back")
        
        d.press("back")
        
        assert d(text=selected_note_text).exists()



t = Test()

setting = Setting(
    apk_path="./apk/omninotes/OmniNotes-6.0.5.apk",
    device_serial="emulator-5554",
    output_dir="output/omninotes/801/mutate/1",
    policy_name="random",

    main_path="main_path/omninotes/801.json"
)
start_kea(t,setting)

