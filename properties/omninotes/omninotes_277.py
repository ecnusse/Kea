import sys
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @initializer()
    def set_up(self):
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/done").click()
        
        if d(text="OK").exists():
            d(text="OK").click()
            
        d(resourceId="it.feio.android.omninotes:id/fab_expand_menu_button").long_click()
        
        d.press("back")
        
        d.press("back")
        
    @mainPath()
    def rule_search_by_tag_should_display_results_mainpath(self):
        d(resourceId="it.feio.android.omninotes:id/fab_expand_menu_button").long_click()
        d(resourceId="it.feio.android.omninotes:id/detail_content").set_text("#")
        d.press("back")
        d.press("back")
        d(resourceId="it.feio.android.omninotes:id/menu_search").click()
        d(resourceId="it.feio.android.omninotes:id/menu_tags").click()

    @precondition(
            lambda self: 
            d(text="Search in notes").exists() and 
            d(resourceId="it.feio.android.omninotes:id/menu_tags").exists() and not 
            d(text="Settings").exists()
            )
    @rule()
    def rule_search_by_tag_should_display_results(self):
        d(resourceId="it.feio.android.omninotes:id/menu_tags").click()
        
        tag_count = int(d(resourceId="it.feio.android.omninotes:id/control").count)
        print("tag_count: " + str(tag_count))
        if tag_count == 0:
            print("no tag, return")
            return
        selected_tag = random.randint(0, tag_count - 1)+1
        selected_tag_name = d(resourceId="it.feio.android.omninotes:id/title")[selected_tag].info['text']
        print("selected_tag: " + str(selected_tag_name))
        note_count = selected_tag_name.rsplit(" ", 1)[1].split("(")[1].split(")")[0]
        d(resourceId="it.feio.android.omninotes:id/title")[selected_tag].click()
        
        d(text="OK").click()
        
        assert d(resourceId="it.feio.android.omninotes:id/root").exists(), "no note"
        assert d(resourceId="it.feio.android.omninotes:id/root").count <= int(note_count), "note count < " + str(note_count)
    


t = Test()

setting = Setting(
    apk_path="./apk/omninotes/5.2.10.apk",
    device_serial="emulator-5554",
    output_dir="../output/omninotes/277/mutate",
    policy_name="mutate",
    
    number_of_events_that_restart_app = 100
)
start_kea(t,setting)

