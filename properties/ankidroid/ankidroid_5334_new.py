import sys
sys.path.append("..")
from kea.core import *

class Test(Kea):
    

    @initializer()
    def set_up(self):
        d(text="Get Started").click()

    @mainPath()
    def text_should_display_after_type_answer_mainpath(self):
        d(resourceId="com.ichi2.anki:id/fab_main").click()
        d(text="Add").click()
        d(resourceId="com.ichi2.anki:id/note_type_spinner").click()
        d(text="Basic (type in the answer)").click()
        d(description="Front").set_text("Hello World")
        d(resourceId="com.ichi2.anki:id/action_save").click()
        d(description="Navigate up").click()
        d(resourceId="com.ichi2.anki:id/deckpicker_name").click()
        d(resourceId="com.ichi2.anki:id/answer_field").set_text("Hello World")

    # 5334
    @precondition(
        lambda self: 
        d(resourceId="com.ichi2.anki:id/new_number").exists() and
        d(resourceId="com.ichi2.anki:id/answer_field").exists() and
        d(resourceId="com.ichi2.anki:id/answer_field").get_text() != "Type answer" and
        d(resourceId="com.ichi2.anki:id/answer_options_layout").exists()
    )
    @rule()
    def text_should_display_after_type_answer(self):
        typed_text = d(resourceId="com.ichi2.anki:id/answer_field").get_text()
        print("typed_text: " + typed_text)
        d(resourceId="com.ichi2.anki:id/answer_options_layout").click()
        
        for view in d(resourceId="content").child(className="android.view.View"):
            print("view text: " + view.get_text())
            if typed_text in view.get_text():
                return True 
        assert False, "text should display after type answer"



if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/ankidroid/2.18alpha6.apk",
        device_serial="emulator-5554",
        output_dir="../output/ankidroid/5334/mutate_new",
        policy_name="random",
        send_document=False
    )
    
