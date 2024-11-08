import sys
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @initializer()
    def set_up(self):
        d(text="Get Started").click()

    @mainPath()
    def filter_by_tag_mainpath(self):
        d(resourceId="com.ichi2.anki:id/deckpicker_name").click()
        d(description="Open drawer").click()
        d(text="Card browser").click()
        d(resourceId="com.ichi2.anki:id/card_sfld").click()

    # 7070
    @precondition(
        lambda self: d(text="Edit note").exists() and
        d(resourceId="com.ichi2.anki:id/CardEditorTagButton").exists() and
        len(d(resourceId="com.ichi2.anki:id/CardEditorTagButton").get_text())>=7
    )
    @rule()
    def filter_by_tag(self):
        tag_info = d(resourceId="com.ichi2.anki:id/CardEditorTagButton").get_text()
        tag_list = tag_info[6:].split(", ")
        tag_name = random.choice(tag_list)
        print("tag_name: "+tag_name)
        deck_name = d(resourceId="com.ichi2.anki:id/CardEditorDeckText").right(resourceId="android:id/text1").get_text()
        print("deck_name: "+deck_name)
        front = d(resourceId="com.ichi2.anki:id/id_note_editText",description="Front").get_text()
        print("front: "+front)
        
        
        d(resourceId="com.ichi2.anki:id/action_save").click()
        
        d(description="More options").click()
        
        d(text="Filter by tag").click()
        
        d(text=tag_name).click()
        
        d(text="Select").click()
        
        assert d(resourceId="com.ichi2.anki:id/card_sfld").exists(), "card not found"



t = Test()

setting = Setting(
    apk_path="./apk/ankidroid/2.18alpha6.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/7070/mutate_new/1",
    policy_name="random"
)
start_kea(t,setting)

