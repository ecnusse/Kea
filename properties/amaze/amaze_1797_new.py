import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    # 1797
    @precondition(lambda self: d(text="Type to search…").exists())
    @rule()
    def rule_search(self):
        
        characters = st.text(alphabet=string.ascii_lowercase,min_size=1, max_size=1).example()
        print("characters: "+str(characters))
        d(text="Type to search…").set_text(characters)
        
        d.set_fastinput_ime(False)
        
        d.send_action("search")
        
        d.set_fastinput_ime(True)
        file_name = d(resourceId="com.amaze.filemanager:id/searchItemFileNameTV")
        if file_name.count == 0:
            print("no file found")
            return
        for i in range(file_name.count):
            assert characters in file_name[i].get_text().lower(), "characters: " + characters + " file_name: " + file_name[i].get_text().lower()




t = Test()

setting = Setting(
    apk_path="./apk/amaze/3.10.apk",
    device_serial="emulator-5554",
    output_dir="output/amaze/1797/1",
    policy_name="random",

)

