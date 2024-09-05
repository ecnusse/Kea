import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @initialize()
    def set_up(self):
        d(text="Get Started").click()

    # 6167
    @precondition(
        lambda self: d(resourceId="com.ichi2.anki:id/card_sfld").exists() and
        d(text="Question").exists() and
        d(text="Answer").exists() and not 
        d(resourceId="com.ichi2.anki:id/card_checkbox").exists()
    )
    @rule()
    def question_and_answer_should_be_consistent(self):
        card = random.choice(d(resourceId="com.ichi2.anki:id/card_item_browser"))
        question = card.child(resourceId="com.ichi2.anki:id/card_sfld").get_text()
        print("question: " + question)
        answer = card.child(resourceId="com.ichi2.anki:id/card_column2").get_text()
        print("answer: " + answer)
        card.click()
        
        front_text = d(description="Front",resourceId="com.ichi2.anki:id/id_note_editText").get_text()
        back_text = d(description="Back",resourceId="com.ichi2.anki:id/id_note_editText").get_text()
        print("front_text: " + str(front_text))
        print("back_text: " + str(back_text))
        assert front_text == question and back_text == answer
        


t = Test()

setting = Setting(
    apk_path="./apk/ankidroid/2.18alpha6.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/6167/mutate_new/1",
    policy_name="random",

    send_document=False,
    main_path="main_path/ankidroid/6167_new.json"
)
run_android_check_as_test(t,setting)

