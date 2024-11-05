import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @initialize()
    def set_up(self):
        if d(text="ALLOW").exists():
            d(text="ALLOW").click()
            
        elif d(text="Allow").exists():
            d(text="Allow").click()
            

    @precondition(lambda self: d(textContains="Search results of").exists() and not 
                  d(resourceId="com.amaze.filemanager:id/telegram").exists() and 
                  d(resourceId="com.amaze.filemanager:id/firstline").exists()
    )
    @rule()
    def rule_search(self):
        search_text = d(textContains="Search results of").get_text()
        print("search_text: " + search_text)
        search_word = search_text.split(" ")[-1]
        print("search_word: " + search_word)
        file_name = d(resourceId="com.amaze.filemanager:id/firstline")
        for i in range(file_name.count):
            assert search_word.lower() in file_name[i].get_text().lower(), "search_word: " + search_word + " file_name: " + file_name[i].get_text()




t = Test()

setting = Setting(
    apk_path="./apk/amaze/amaze-3.5.0.apk",
    device_serial="emulator-5554",
    output_dir="output/amaze/1797/random_100/1",
    policy_name="random",

    main_path="main_path/amaze/1797.json"
)
start_kea(t,setting)

