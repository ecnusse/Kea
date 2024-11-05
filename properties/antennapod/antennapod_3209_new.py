from kea.main import *
import time
import sys


class Test(Kea):
    

    @initialize()
    def set_up(self):
        pass

    @precondition(
        lambda self: d(resourceId="de.danoeh.antennapod:id/toolbar").exists() and 
        d(resourceId="de.danoeh.antennapod:id/toolbar").child(text="Episodes",className="android.widget.TextView").exists() and
        d(resourceId="de.danoeh.antennapod:id/txtvTitle").exists() and not 
        d(resourceId="de.danoeh.antennapod:id/navDrawerFragment").exists() and not 
        d(text="Filtered").exists()
    )
    @rule()
    def remove_or_add_favorite(self):
        selected_title = random.choice(d(resourceId="de.danoeh.antennapod:id/txtvTitle"))
        selected_title_name = selected_title.info['text']
        print("title: " + selected_title_name)
        selected_title.long_click()
        
        remove_or_add = True
        if d(text="Remove from favorites").exists():
            print("remove")
            d(text="Remove from favorites").click()
        else:
            print("add")
            d(text="Add to favorites").click()
            remove_or_add = False
        
        if remove_or_add:
            assert not d(text=selected_title_name).exists() or not d(text=selected_title_name).sibling(resourceId="de.danoeh.antennapod:id/status").child(resourceId="de.danoeh.antennapod:id/isFavorite").exists(), "remove failed"
        else:
            assert d(text=selected_title_name).sibling(resourceId="de.danoeh.antennapod:id/status").child(resourceId="de.danoeh.antennapod:id/isFavorite").exists(), "add failed"





t = Test()

setting = Setting(
    apk_path="./apk/antennapod/3.2.0.apk",
    device_serial="emulator-5554",
    output_dir="output/antennapod/3209/mutate_new/1",
    policy_name="random",
    timeout=86400,
    number_of_events_that_restart_app = 100,
    main_path="main_path/antennapod/3209_new.json"
)
start_kea(t,setting)

