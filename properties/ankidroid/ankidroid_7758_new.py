import sys
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @initialize()
    def set_up(self):
        d(description="Navigate up").click()
        
        d(text="Settings").click()
        
        d(text="AnkiDroid").click()
        
        d(text="Language").click()
        
        d(scrollable=True).scroll.to(text="日本語")
        
        d(text="日本語").click()

    @main_path()
    def card_info_should_be_translated_mainpath(self):
        d(description="前に戻る").click()
        d(text="カードブラウザ").click()
        d(resourceId="com.ichi2.anki:id/dropdown_deck_name").click()
        d(text="全てのデッキ").click()

    @precondition(
        lambda self: d(resourceId="com.ichi2.anki:id/card_sfld").exists() and 
        d(resourceId="com.ichi2.anki:id/action_search").exists() 
    )
    @rule()
    def card_info_should_be_translated(self):
        d(resourceId="com.ichi2.anki:id/card_sfld").long_click()
        
        d(resourceId="com.ichi2.anki:id/toolbar").child(className="android.widget.ImageView").click()
        
        assert not d(text="Card Info").exists(), "Card Info found"




t = Test()

setting = Setting(
    apk_path="./apk/ankidroid/2.18alpha6.apk",
    device_serial="emulator-5554",
    output_dir="output/ankidroid/7758/mutate/1",
    policy_name="random"
)
run_android_check_as_test(t,setting)

