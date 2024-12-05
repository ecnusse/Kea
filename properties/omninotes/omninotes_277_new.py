import sys
sys.path.append("..")
from kea.core import *

class Test(Kea):
    

    @initializer()
    def set_up(self):
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/done").click()

    @mainPath()
    def rule_search_by_tag_should_display_results_mainpath(self):
        d(resourceId="it.feio.android.omninotes:id/fab_expand_menu_button").long_click()
        d(resourceId="it.feio.android.omninotes:id/detail_content").set_text("#hello")
        d.press("back")
        d.press("back")
        d(resourceId="it.feio.android.omninotes:id/menu_search").click()
        d(resourceId="it.feio.android.omninotes:id/menu_tags").click()

    # bug 277
    @precondition(
            lambda self: 
            d(text="Select tag(s)").exists() and 
            d(resourceId="android:id/text1").exists() and
            d(text="OK").exists()
            )
    @rule()
    def rule_search_by_tag_should_display_results(self):
        
        tag_count = int(d(resourceId="android:id/text1").count)
        print("tag_count: " + str(tag_count))
        if tag_count == 0:
            print("no tag, return")
            return
        selected_tag = random.randint(0, tag_count - 1)
        selected_tag_text = d(resourceId="android:id/text1")[selected_tag].info['text']
        selected_tag_name = selected_tag_text.rsplit(" ", 1)[0]
        print("selected_tag: " + str(selected_tag_name))
        note_count = selected_tag_text.rsplit(" ", 1)[1].split("(")[1].split(")")[0]
        
        d(resourceId="android:id/text1")[selected_tag].click()
        
        d(text="OK").click()
        
        if d(resourceId="it.feio.android.omninotes:id/menu_attachment").exists():
            print("wrong page, return")
            return
        if "," in d(resourceId="it.feio.android.omninotes:id/search_query").info['text']:
            print("multiple tag, return")
            return
        assert d(resourceId="it.feio.android.omninotes:id/root").exists(), "no note"
        assert d(resourceId="it.feio.android.omninotes:id/root").count <= int(note_count), "note count < " + str(note_count)
        random.choice(d(resourceId="it.feio.android.omninotes:id/note_title")).click()
        
        assert d(text=selected_tag_name).exists(), "no tag"

        


if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/omninotes/OmniNotes-6.3.0.apk",
        device_serial="emulator-5554",
        output_dir="../output/omninotes/277/guided_new",
        policy_name="guided"
    )
    start_kea(t,setting)
    
