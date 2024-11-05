import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
     

    @precondition(
        lambda self: d(resourceId="com.ichi2.anki:id/new_number").exists() and 
        d(description="More options").exists()
    )
    @rule()
    def add_new_card_should_update_new_card_count(self):
        original_card_count = int(d(resourceId="com.ichi2.anki:id/new_number").get_text())
        print("original_card_count: " + str(original_card_count))
        d(description="More options").click()
        
        d(text="Edit note").click()
        
        d(description="More options").click()
        
        d(text="Add note").click()
        
        front = st.text(alphabet=string.ascii_letters,min_size=1, max_size=6).example()
        print("front: " + str(front))
        d(resourceId="com.ichi2.anki:id/id_note_editText").set_text(front)
        
        d(resourceId="com.ichi2.anki:id/action_save").click()
        
        d.press("back")
        
        new_card_count = int(d(resourceId="com.ichi2.anki:id/new_number").get_text())
        print("new_card_count: " + str(new_card_count))
        assert new_card_count == original_card_count + 1, "new card count should increase by 1"




t = Test()

setting = Setting(
    apk_path="./apk/ankidroid/2.12.1.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/6887/mutate/1",
    policy_name="random",

    main_path="main_path/ankidroid/6887.json"
)
start_kea(t,setting)

