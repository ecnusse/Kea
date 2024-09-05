import string
import sys
import time
sys.path.append("..")
from kea.main import *
from hypothesis import strategies as st
class Test(Kea):
    

    @initialize()
    def set_up(self):
        pass

    @precondition(
        lambda self: d(resourceId="com.ichi2.anki:id/card_sfld").exists() and 
        d(description="More options").exists() and 
        d(resourceId="com.ichi2.anki:id/action_search").exists() and 
        d(resourceId="com.ichi2.anki:id/card_column2").exists()
    )
    @rule()
    def edit_card_should_remember_scroll_position(self):
        selected_card = d(resourceId="com.ichi2.anki:id/card_column2")[0].get_text()
        print("selected_card: " + str(selected_card))
        edit_card = random.choice(d(resourceId="com.ichi2.anki:id/card_sfld"))
        edit_card.long_click()
        
        d(description="More options").click()
        
        d(text="Edit note").click()
        
        new_front = st.text(alphabet=string.ascii_letters,min_size=1, max_size=3).example()
        print("new_front: " + str(new_front))
        d(resourceId="com.ichi2.anki:id/id_note_editText").set_text(new_front)
        
        d(resourceId="com.ichi2.anki:id/action_save").click()
        
        assert d(resourceId="com.ichi2.anki:id/card_column2")[0].get_text() == selected_card, "scroll position should not change"


t = Test()

setting = Setting(
    apk_path="./apk/ankidroid/2.12.1.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/6857/mutate/1",
    policy_name="random",

    main_path="main_path/ankidroid/6857.json"
)
run_android_check_as_test(t,setting)

