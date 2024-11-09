import sys
sys.path.append("..")
from kea.main import *

class Test(Kea):

    @mainPath()
    def question_and_answer_should_be_consistent_mainpath(self):
        d(resourceId="com.ichi2.anki:id/fab_expand_menu_button").click()
        d(text="Add").click()
        d(description="Front").set_text("Hello World")
        d(resourceId="com.ichi2.anki:id/id_note_editText", description="Back").set_text("Hello")
        d(resourceId="com.ichi2.anki:id/action_save").click()
        d(description="Navigate up").click()
        d(text="Card browser").click()

    @precondition(
        lambda self: d(resourceId="com.ichi2.anki:id/card_sfld").exists() and
        d(text="Question").exists() and
        d(text="Answer").exists() 
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
    apk_path="./apk/ankidroid/2.10.apk",
    device_serial="emulator-5554",
    output_dir="../output/ankidroid/6167/mutate",
    policy_name="mutate",
    send_document=False
)
start_kea(t,setting)

