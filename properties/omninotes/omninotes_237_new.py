import string
import sys
sys.path.append("..")
from kea.core import *

class Test(Kea):
    

    # @initializer()
    # def set_up(self):
    #     if d(text="OK").exists():
    #         d(text="OK").click()
            
    #     d(resourceId="it.feio.android.omninotes:id/next").click()
        
    #     d(resourceId="it.feio.android.omninotes:id/next").click()
        
    #     d(resourceId="it.feio.android.omninotes:id/next").click()
        
    #     d(resourceId="it.feio.android.omninotes:id/next").click()
        
    #     d(resourceId="it.feio.android.omninotes:id/next").click()
        
    #     d(resourceId="it.feio.android.omninotes:id/done").click()
        
    #     if d(text="OK").exists():
    #         d(text="OK").click()

    @mainPath()
    def hash_tag_with_number_start_shouldbe_recognized_mainpath(self):
        d(resourceId="it.feio.android.omninotes:id/fab_expand_menu_button").long_click()

    @precondition(lambda self: d(resourceId="it.feio.android.omninotes:id/menu_attachment").exists() and d(resourceId="it.feio.android.omninotes:id/menu_share").exists() and d(resourceId="it.feio.android.omninotes:id/menu_tag").exists() )
    @rule()
    def hash_tag_shouldbe_recognized(self):
        
        text = st.text(alphabet=string.ascii_letters,min_size=2, max_size=5).example()
        tag = "#"+ text
        print("tag: " + tag)
        if d(className="android.widget.CheckBox").exists():
            print("checkbox exists")
            d(className="android.widget.CheckBox").sibling(className="android.widget.EditText").set_text(tag)
        else:
            d(resourceId="it.feio.android.omninotes:id/detail_content").set_text(tag)
        
        d(resourceId="it.feio.android.omninotes:id/toolbar").child(className="android.widget.ImageButton").click()
        

        note_count = int(d(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root").count)
        selected_note = random.randint(0, note_count - 1)
        selected_note_name = d(resourceId="it.feio.android.omninotes:id/note_title")[selected_note].info['text']
        print("selected_note: " + str(selected_note_name))
        
        d(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root")[selected_note].click()
        
        d(resourceId="it.feio.android.omninotes:id/menu_tag").click()
        
        assert d(resourceId="it.feio.android.omninotes:id/md_title",textContains=text).exists()



if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/omninotes/OmniNotes-6.3.0.apk",
        device_serial="emulator-5554",
        output_dir="../output/omninotes/237/guided_new",
        policy_name="guided"
    )
    start_kea(t,setting)
    
