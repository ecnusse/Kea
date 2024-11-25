import sys
sys.path.append("..")
from kea.core import *

class Test(Kea):
    

    @initializer()
    def set_up(self):
        if d(text="ALLOW").exists():
            d(text="ALLOW").click()
            
        elif d(text="Allow").exists():
            d(text="Allow").click()
            
            
    # bug #3560  
    @precondition(lambda self: d(resourceId="com.amaze.filemanager:id/firstline").exists() and 
                  d(resourceId="com.amaze.filemanager:id/sd_main_fab").exists() and not 
                  d(resourceId="com.amaze.filemanager:id/snackBarCardView").exists() and not
                  d(resourceId="com.amaze.filemanager:id/donate").exists() and not 
                  d(resourceId="com.amaze.filemanager:id/check_icon").exists() and not 
                  d(resourceId="com.amaze.filemanager:id/search_edit_text").exists() and not
                  d(resourceId="com.amaze.filemanager:id/snackBarConstraintLayout").exists()
                  )
    @rule()
    def rule_open_folder(self):
        
        count = d(resourceId="com.amaze.filemanager:id/firstline").count
        print("count: "+str(count))
        index = random.randint(0, count-1)
        print("index: "+str(index))
        selected_file = d(resourceId="com.amaze.filemanager:id/firstline")[index]
        selected_file_name = selected_file.get_text()
        print("selected file or dir name: "+str(selected_file_name))
        selected_file.right(resourceId="com.amaze.filemanager:id/properties").click()
        
        if d(text="Open with").exists():
            print("its a file, not a folder")
            return
        d.press("back")
        
        selected_file.click()
        
        full_path = d(resourceId="com.amaze.filemanager:id/fullpath").get_text()
        print("full path: "+str(full_path))     
        assert selected_file_name in full_path
        d.press("back")



if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/amaze/3.10.apk",
        device_serial="emulator-5554",
        output_dir="../output/amaze/3560/random_100/1",
        policy_name="random",
        
        number_of_events_that_restart_app = 100
    )
    start_kea(t,setting)
    
