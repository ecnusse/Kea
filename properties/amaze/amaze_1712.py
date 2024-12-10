import sys
sys.path.append("..")
from kea import *

class Test(KeaTest):
    

    @initializer()
    def set_up(self):
        if d(text="ALLOW").exists():
            d(text="ALLOW").click()
            
        elif d(text="Allow").exists():
            d(text="Allow").click()
            
    
    @precondition(lambda self: d(resourceId="com.amaze.filemanager:id/firstline").exists() and 
                  d(resourceId="com.amaze.filemanager:id/sd_main_fab").exists() and not
                  d(resourceId="com.amaze.filemanager:id/donate").exists())
    @rule()
    def rule_hide_unhide_file(self):
        
        # first hide a file or folder
        count = d(resourceId="com.amaze.filemanager:id/firstline").count
        print("count: "+str(count))
        index = random.randint(0, count-1)
        print("index: "+str(index))
        selected_file = d(resourceId="com.amaze.filemanager:id/firstline")[index]
        selected_file_name = selected_file.get_text()
        print("selected file name: "+str(selected_file_name))
        selected_file.long_click()
        
        d(description="More options").click()
        
        d(text="Hide").click()
        
        assert not d(text=selected_file_name).exists()
        
        # unhide a file or folder
        d(description="More options").click()
        
        d(text="Hidden Files").click()
        
        d(text=selected_file_name).right(resourceId="com.amaze.filemanager:id/delete_button").click()
        
        d(text="CLOSE").click()
        
        assert d(text=selected_file_name).exists(), "unhide file failed with file name: " + str(selected_file_name)



if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/amaze/amaze-3.4.3.apk",
        device_serial="emulator-5554",
        output_dir="../output/amaze/1712/guided/1",
        policy_name="random",
    )
    start_kea(t,setting)
    
