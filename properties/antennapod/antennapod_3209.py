import sys
sys.path.append("..")
from kea.main import *

class Test(Kea):

    @main_path()
    def remove_favorite_mainpath(self):
        d(text="Add Podcast").click()
        d(text="SEARCH ITUNES").click()
        d(resourceId="de.danoeh.antennapod:id/txtvTitle").click()
        d(text="SUBSCRIBE").click()
        d.press("back")
        d.press("back")
        d(description="Open menu").click()
        d(text="Episodes").click()
        d(text="ALL").click()
        d(resourceId="de.danoeh.antennapod:id/txtvTitle").long_click()
        d(text="Add to Favorites").click()
        d(text="FAVORITES").click()

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
    output_dir="../output/antennapod/3209/mutate",
    policy_name="mutate"
)
start_kea(t,setting)

