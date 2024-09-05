import string
import sys
import time
sys.path.append("..")
from kea.main import *

class Test(Kea):
    

    @precondition(
        lambda self: d(text="Settings").exists() and d(text="Behavior").exists()
    )
    @rule()
    def import_an_backup_should_take_effect(self):
        # first backup
        d(scrollable=True).scroll.to(text="Export database")
        
        d(text="Export database").click()
        backup_title = st.text(alphabet=string.ascii_letters,min_size=1, max_size=5).example()
        print("backup title: " + backup_title)
        d(text="ActivityDiary_Export.sqlite3").set_text(backup_title)
        
        d(text="SAVE").click()
        
        d.press("back")
        # then delete an activity
        # random select an activity
        activity_count = d(resourceId="de.rampro.activitydiary:id/select_card_view").count
        random_index = random.randint(0, activity_count - 1)
        selected_activity = d(resourceId="de.rampro.activitydiary:id/select_card_view")[random_index]
        
        
        selected_activity.click()
        
        activity_name = selected_activity.child(resourceId="de.rampro.activitydiary:id/activity_name").get_text()
        print("activity name: " + activity_name)
        selected_activity.long_click()
        
        d(resourceId="de.rampro.activitydiary:id/action_edit_delete").click()
        
        # then import
        d(description="Open navigation").click()
        
        d(text="Settings").click()
        
        d(scrollable=True).scroll.to(text="Import database")
        
        d(text="Import database").click()
        
        d(text=backup_title).click()
        
        d.press("back")
        
        assert d(text=activity_name).exists(), "activity not exist after import" + str(activity_name)


t = Test()

setting = Setting(
    apk_path="./apk/activitydiary/1.4.2.apk",
    device_serial="emulator-5554",
    output_dir="output/activitydiary/176/1",
    policy_name="random",

)

