import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @initialize()
    def set_up(self):
        d(text="Get Started").click()

    # 5352
    @precondition(
        lambda self: d(text="Manage note types").exists() and 
        d(resourceId="com.ichi2.anki:id/note_type_add").exists() and
        d(resourceId="com.ichi2.anki:id/note_name").exists()
    )
    @rule()
    def note_type_should_be_consistent(self):
        d(resourceId="com.ichi2.anki:id/note_name").click()
        
        d(resourceId="com.ichi2.anki:id/action_add_new_model").click()
        
        type_name = st.text(alphabet=string.printable,min_size=1, max_size=6).example()
        print("type_name: " + str(type_name))
        d(className="android.widget.EditText").set_text(type_name)
        
        d(text="OK").click()
        
        assert d(resourceId="com.ichi2.anki:id/note_type_editor_fields").child_by_text(type_name, allow_scroll_search=True).exists, "new note type should be added"



t = Test()

setting = Setting(
    apk_path="./apk/ankidroid/2.18alpha6.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/5352/mutate_new/1",
    policy_name="random",

    main_path="main_path/ankidroid/5352_new.json"
)
run_android_check_as_test(t,setting)

