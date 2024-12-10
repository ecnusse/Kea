import sys
sys.path.append("..")
from kea import *

class Test(KeaTest):

    @initializer()
    def set_up(self):
        d(text="Get Started").click()

    @mainPath()
    def card_should_be_searched_in_all_decks_mainpath(self):
        d(resourceId="com.ichi2.anki:id/deckpicker_name").click()
        d(description="Open drawer").click()
        d(text="Card browser").click()

    # 8975
    @precondition(
        lambda self: d(resourceId="com.ichi2.anki:id/action_search").exists() and 
        d(resourceId="com.ichi2.anki:id/card_sfld").exists() and not
        d(resourceId="com.ichi2.anki:id/search_close_btn").exists()
    )
    @rule()
    def card_should_be_searched_in_all_decks(self):
        text = d(resourceId="com.ichi2.anki:id/card_sfld").get_text()
        print("text: " + str(text))
        # random select a substring of the text
        selected_text = random.choice(text.split(" "))
        print("selected_text: " + str(selected_text))
        
        d(resourceId="com.ichi2.anki:id/dropdown_deck_name").click()
        
        d(text="Default").click()
        
        d(resourceId="com.ichi2.anki:id/action_search").click()
        
        d(resourceId="com.ichi2.anki:id/search_src_text").set_text(selected_text)
        
        d.set_fastinput_ime(False) 
        d.send_action("search") 
        
        d(text="Search all decks").click()
        
        assert d(resourceId="com.ichi2.anki:id/card_sfld").exists(), "card not found"



if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/ankidroid/2.18alpha6.apk",
        device_serial="emulator-5554",
        output_dir="output/ankidroid/8975/guided_new/1",
        policy_name="random"
    )
    start_kea(t,setting)
    
