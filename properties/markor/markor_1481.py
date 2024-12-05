import string
from kea.core import *

class Test(Kea):
    

    @initializer()
    def set_up(self):
        d(resourceId="net.gsantner.markor:id/next").click()
        
        d(resourceId="net.gsantner.markor:id/next").click()
        
        d(resourceId="net.gsantner.markor:id/next").click()
        
        d(resourceId="net.gsantner.markor:id/next").click()
        
        d(resourceId="net.gsantner.markor:id/next").click()
        
        d(text="DONE").click()
        
        
    
    @precondition(
        lambda self: d(
            resourceId="net.gsantner.markor:id/fab_add_new_item"
        ).exists()
    )
    @rule()
    def rule_rename_file(self):
        file_count = d(resourceId="net.gsantner.markor:id/opoc_filesystem_item__title").count
        print("file count: "+str(file_count))
        if file_count == 0:
            print("no file to rename")
            return
        file_index = random.randint(0, file_count - 1)
        selected_file = d(resourceId="net.gsantner.markor:id/opoc_filesystem_item__title")[file_index]
        file_name = selected_file.info['text']
        is_file = True
        if "." not in file_name:
            is_file = False
            print("not a file")
            return
        file_name_suffix = file_name.split(".")[-1]
        print("file name: "+str(file_name))
        selected_file.long_click()
        
        d(resourceId="net.gsantner.markor:id/action_rename_selected_item").click()
        
        name = st.text(alphabet=string.ascii_letters,min_size=1, max_size=6).example()
        if is_file:
            name = name+"."+file_name_suffix
        print("new file name: "+str(name))
        d(resourceId="net.gsantner.markor:id/new_name").set_text(name)
        
        d(text="OK").click()
        
        assert d(resourceId="net.gsantner.markor:id/ui__filesystem_dialog__list").child_by_text(name,allow_scroll_search=True).exists()



if __name__ == "__main__":
    t = Test()
    setting = Setting(
        apk_path="./apk/markor/2.11.1.apk",
        device_serial="emulator-5554",
        output_dir="../output/markor/1481/guided",
        policy_name="guided",
        
        number_of_events_that_restart_app = 10
    )
    start_kea(t,setting)
    
