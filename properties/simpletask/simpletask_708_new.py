import string
import sys
sys.path.append("..")
from kea.core import *

class Test(Kea):
    

    @initializer()
    def set_up(self):
        if d(text="OK").exists():
            d(text="OK").click()

    @precondition(
        lambda self: int(d(resourceId="nl.mpcjanssen.simpletask:id/tasktext").count) > 0 and not d(text="Quick filter").exists() and not d(text="Settings").exists() and not d(text="Saved filters").exists())
    @rule()
    def add_tag(self):
        task_count = int(d(resourceId="nl.mpcjanssen.simpletask:id/tasktext").count)
        print("task count: "+str(task_count))
        selected_task = random.randint(0, task_count - 1)
        print("selected task: "+str(selected_task))
        selected_task = d(resourceId="nl.mpcjanssen.simpletask:id/tasktext")[selected_task]
        selected_task_name = selected_task.get_text()
        print("selected task name: "+str(selected_task_name))
        selected_task.click()
        
        d(resourceId="nl.mpcjanssen.simpletask:id/update").click()
        
        d(resourceId="nl.mpcjanssen.simpletask:id/btnProject").click()
        
        tag_name = st.text(alphabet=string.ascii_letters,min_size=1, max_size=6).example()
        print("tag name: "+str(tag_name))
        d(resourceId="nl.mpcjanssen.simpletask:id/new_item_text").set_text(tag_name)
        
        d.set_fastinput_ime(False)
        
        d(resourceId="com.google.android.inputmethod.latin:id/key_pos_ime_action").click()
        
        d.set_fastinput_ime(True)
        
        d(text="OK").click()
        content = d(resourceId="nl.mpcjanssen.simpletask:id/taskText").get_text()
        print("content: "+str(content))
        
        assert tag_name in content



if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/simpletask/11.0.1.apk",
        device_serial="emulator-5554",
        output_dir="../output/simpletask/mutate_new",
        policy_name="mutate",
    
    )
    start_kea(t,setting)
    
    
