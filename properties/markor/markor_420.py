import string
from kea.main import *
import time
import sys
import re

class Test(Kea):
    

    @initialize()
    def set_up(self):      
        if d(text="OK").exists():
            d(text="OK").click()
        
    @precondition(lambda self: d(text="Select entries").exists() and 
                  d(resourceId="net.gsantner.markor:id/note_title").exists()
                  )
    @rule()
    def selection_should_discard_after_clicking_new(self):
        selected_info = d(resourceId="net.gsantner.markor:id/action_bar_subtitle").get_text()
        number_of_selected = selected_info.split(" ")[0]
        if number_of_selected == "One":
            number_of_selected = 1
        number_of_selected = int(number_of_selected)
        random.choice(d(resourceId="net.gsantner.markor:id/note_title")).click()
        
        if d(text="Select entries").exists():
            new_selected_info = d(resourceId="net.gsantner.markor:id/action_bar_subtitle").get_text()
            new_number_of_selected = new_selected_info.split(" ")[0]
            if new_number_of_selected == "One":
                new_number_of_selected = 1
            new_number_of_selected = int(new_number_of_selected)
            assert new_number_of_selected == number_of_selected - 1 or new_number_of_selected == number_of_selected + 1, "number of selected not correct"

        


t = Test()

setting = Setting(
    apk_path="./apk/markor/1.3.0.apk",
    device_serial="emulator-5554",
    output_dir="output/markor/420/mutate/1",
    policy_name="random",

    main_path="main_path/markor/420.json"
)
start_kea(t,setting)

