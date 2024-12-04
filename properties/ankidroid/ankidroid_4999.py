import sys
sys.path.append("..")
from kea.core import *

class Test(Kea):

    @precondition(
        lambda self: d(resourceId="com.ichi2.anki:id/deckpicker_name").exists() and 
        d(resourceId="com.ichi2.anki:id/fab_expand_menu_button").exists() 
    )
    @rule()
    def card_browser_should_display_just_selected_deck(self):
        selected_deck = random.choice(d(resourceId="com.ichi2.anki:id/deckpicker_name"))
        selected_deck_name = selected_deck.get_text()
        print("selected_deck_name: " + str(selected_deck_name))
        selected_deck.click()
        
        d.press("back")
        
        d(description="Navigate up").click()
        
        d(text="Card browser").click()
        
        deck_name = d(resourceId="com.ichi2.anki:id/dropdown_deck_name").get_text()
        print("deck_name: " + str(deck_name))        
        assert deck_name == selected_deck_name or selected_deck_name in deck_name, "deck name should be the same"




if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/ankidroid/2.8.4.apk",
        device_serial="emulator-5554",
        output_dir="../output/ankidroid/4999/guided",
        policy_name="guided"
    )
    start_kea(t,setting)
    
