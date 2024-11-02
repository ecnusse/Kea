import string
import sys
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @initialize()
    def set_up(self):
        if d(text="ALLOW").exists():
            d(text="ALLOW").click()
            
        elif d(text="Allow").exists():
            d(text="Allow").click()
            

    @precondition(lambda self: d(resourceId="com.amaze.filemanager:id/firstline").exists()and
                not d(resourceId="com.amaze.filemanager:id/design_menu_item_action_area").exists())
    @rule()
    def rule_rename(self):

        
        count = d(resourceId="com.amaze.filemanager:id/firstline").count
        print("count: "+str(count))
        index = random.randint(0, count-1)
        print("index: "+str(index))
        selected_file = d(resourceId="com.amaze.filemanager:id/firstline")[index]
        selected_file_name = selected_file.get_text()
        print("selected file name: "+str(selected_file_name))
        selected_file.right(resourceId="com.amaze.filemanager:id/properties").click()
        
        d(text="Rename").click()
        
        new_file_name = st.text(alphabet=string.ascii_letters,min_size=1, max_size=5).example()
        print("new file name: "+str(new_file_name))
        d(resourceId="com.amaze.filemanager:id/singleedittext_input").set_text(new_file_name)
        
        d(text="SAVE").click()
        
        assert not d(text=selected_file_name).exists(), "rename failed with new_file_name: " + new_file_name
    



t = Test()

setting = Setting(
    apk_path="./apk/amaze/amaze-3.3.2.apk",
    device_serial="emulator-5554",
    output_dir="output/amaze/1556/random_100/1",
    policy_name="random",

    number_of_events_that_restart_app = 100
)
run_android_check_as_test(t,setting)

