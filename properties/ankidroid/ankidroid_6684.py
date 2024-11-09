import string
import sys
sys.path.append("..")
from kea.main import *

class Test(Kea):
    
    @mainPath()
    def cloze_should_work_mainpath(self):
        d(resourceId="com.ichi2.anki:id/fab_expand_menu_button").click()

    @precondition(
        lambda self: d(text="Add").exists() and 
        d(text="Get shared decks").exists() 
    )
    @rule()
    def cloze_should_work(self):
        d(text="Add").click()
        
        d(resourceId="com.ichi2.anki:id/note_type_spinner").click()
        
        d(text="Cloze").click()
        from hypothesis import strategies as st
        text = st.text(alphabet=string.ascii_letters,min_size=1, max_size=6).example() + "{{c1::cloze}}"
        d(description="Text").set_text(text)
        
        d(resourceId="com.ichi2.anki:id/action_preview").click()
        
        assert not d(text="help").exists, "help shouldnot exist"




t = Test()

setting = Setting(
    apk_path="./apk/ankidroid/2.12.0beta6.apk",
    device_serial="emulator-5554",
    output_dir="../output/ankidroid/6684/mutate",
    policy_name="mutate"
)
start_kea(t,setting)

