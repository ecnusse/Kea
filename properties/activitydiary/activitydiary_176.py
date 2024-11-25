import sys
sys.path.append("..")
from kea.core import *

class Test(Kea):
    

    @precondition(
        lambda self: d(text="Activity Diary").exists() and d(resourceId="de.rampro.activitydiary:id/select_card_view").exists() and not d(text="Settings").exists()
    )
    @rule()
    def long_click_activity_should_edit_it(self):
        # random select an activity
        activity_count = d(resourceId="de.rampro.activitydiary:id/select_card_view").count
        random_index = random.randint(0, activity_count - 1)
        selected_activity = d(resourceId="de.rampro.activitydiary:id/select_card_view")[random_index]
        activity_name = selected_activity.child(resourceId="de.rampro.activitydiary:id/activity_name").get_text()
        print("activity name: " + activity_name)
        
        selected_activity.long_click()
        
        current_activity_name = d(resourceId="de.rampro.activitydiary:id/edit_activity_name").get_text()
        assert current_activity_name == activity_name, "activity name not match "+ str(activity_name) + " " + str(current_activity_name)

if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/activitydiary/1.2.5.apk",
        device_serial="emulator-5554",
        output_dir="output/activitydiary/176/mutate/1",
        policy_name="random"
    )
    start_kea(t,setting)
    
