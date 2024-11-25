import sys
sys.path.append("..")
from kea.core import *

class Test(Kea):

    @mainPath()
    def card_should_be_searched_in_all_decks_mainpath(self):
        d(resourceId="com.ichi2.anki:id/deckpicker_name").click()
        d(description="Navigate up").click()
        d(text="Card browser").click()

    @precondition(
        lambda self: d(resourceId="com.ichi2.anki:id/action_search").exists() and 
        d(resourceId="com.ichi2.anki:id/card_sfld").exists() 
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
        
        d.set_fastinput_ime(False) # 
        d.send_action("search") # 
        
        d(text="SEARCH ALL DECKS").click()
        
        assert d(resourceId="com.ichi2.anki:id/card_sfld").exists(), "card not found"



if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/ankidroid/2.15.2.apk",
        device_serial="emulator-5554",
        output_dir="../output/ankidroid/8975/mutate",
        policy_name="mutate"
    )
    start_kea(t,setting)
    
