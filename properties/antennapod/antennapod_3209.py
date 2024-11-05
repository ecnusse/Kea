import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @precondition(
        lambda self: d(text="FAVORITES").exists() and d(text="FAVORITES").info['selected'] and d(resourceId="de.danoeh.antennapod:id/txtvTitle").exists() and not d(resourceId="de.danoeh.antennapod:id/nav_list").exists()
    )
    @rule()
    def remove_favorite(self):

        selected_title = random.choice(d(resourceId="de.danoeh.antennapod:id/container"))
        selected_title_name = selected_title.child(resourceId="de.danoeh.antennapod:id/txtvTitle").info['text']
        print("title: " + selected_title_name)
        selected_title.long_click()
        
        d(text="Remove from Favorites").click()
        
        assert not (d(resourceId="de.danoeh.antennapod:id/container").exists() and 
                    d(resourceId="de.danoeh.antennapod:id/container").child(resourceId="de.danoeh.antennapod:id/txtvTitle", text=selected_title_name).exists())


t = Test()

setting = Setting(
    apk_path="./apk/antennapod/1.7.2b.apk",
    device_serial="emulator-5554",
    output_dir="output/antennapod/3209/mutate/1",
    policy_name="random",

    main_path="main_path/antennapod/3209.json"
)
start_kea(t,setting)

