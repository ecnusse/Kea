import sys
import re
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @initializer()
    def set_up(self):
        if d(text="OK").exists():
            d(text="OK").click()
            
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/next").click()
        
        d(resourceId="it.feio.android.omninotes:id/done").click()
        
        if d(text="OK").exists():
            d(text="OK").click()

    @mainPath()
    def hash_tag_with_number_start_shouldbe_recognized_mainpath(self):
        d(resourceId = "it.feio.android.omninotes:id/fab_expand_menu_button").long_click()
    
    def check_hash_tag_exist(self):
        
        for content in d(resourceId="it.feio.android.omninotes:id/note_content"):
            content = content.get_text()
            if "#" not in content:
                continue
            matches = re.findall(r'#(\w+)', content) 
            tags = [m for m in matches if content.find("#"+m)==0 or content[content.find("#"+m)-1].isspace()]
            print("tags: " + str(tags))
            if len(tags) == 0:
                continue
            return True
        
        for title in d(resourceId="it.feio.android.omninotes:id/note_title"):
            title = title.get_text()
            if "#" not in title:
                continue
            matches = re.findall(r'#(\w+)', title) 
            tags = [m for m in matches if title.find("#"+m)==0 or title[title.find("#"+m)-1].isspace()]
            print("tags: " + str(tags))
            if len(tags) == 0:
                continue
            return True
        
        return False



    @precondition(lambda self: d(resourceId="it.feio.android.omninotes:id/note_content").exists() and not
                  d(text="SETTINGS").exists() and
                  self.check_hash_tag_exist() and not
                  d(resourceId="it.feio.android.omninotes:id/action_mode_close_button").exists()
    )
    @rule()
    def hash_tag_with_number_start_shouldbe_recognized(self):

        hashtag_UI_element = []
        for note_content in d(resourceId="it.feio.android.omninotes:id/note_content"):
            content = note_content.get_text()
            if "#" not in content:
                continue
            matches = re.findall(r'#(\w+)', content)
            print("matches: " + str(matches))
            tags = [m for m in matches if content.find("#"+m)==0 or content[content.find("#"+m)-1].isspace()]
            print("tags: " + str(tags))
            if len(tags) == 0:
                continue
            hashtag = tags
            hashtag_UI_element.append((note_content,hashtag))

        for note_title in d(resourceId="it.feio.android.omninotes:id/note_title"):
            title = note_title.get_text()
            if "#" not in title:
                continue
            matches = re.findall(r'#(\w+)', title)
            print("matches: " + str(matches))
            tags = [m for m in matches if title.find("#"+m)==0 or title[title.find("#"+m)-1].isspace()]
            print("tags: " + str(tags))
            if len(tags) == 0:
                continue
            hashtag = tags
            hashtag_UI_element.append((note_title,hashtag))

        selected = random.choice(hashtag_UI_element)
        selected_hashtag_UI_element =selected[0]
        selected_hashtag = selected[1]
        selected_hashtag_UI_element.click()

        d(resourceId="it.feio.android.omninotes:id/menu_tag").click()

        for tag in selected_hashtag:
            assert d(resourceId="it.feio.android.omninotes:id/title",textContains=tag).exists(), "tag not found"



t = Test()

setting = Setting(
    apk_path="./apk/omninotes/OmniNotes-5.1.0.apk",
    device_serial="emulator-5554",
    output_dir="../output/omninotes/237/mutate",
    policy_name="mutate",
    
    number_of_events_that_restart_app = 100
)
start_kea(t,setting)

