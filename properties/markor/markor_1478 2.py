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
        
        
        if d(text="OK").exists():
            d(text="OK").click()

    @mainPath()
    def view_file_should_exist_in_recent_viewed_documents_mainpath(self):
        d(resourceId="net.gsantner.markor:id/fab_add_new_item").click()
        d(resourceId="net.gsantner.markor:id/new_file_dialog__name").set_text("Hello")
        d(text="OK").click()
        d(resourceId="net.gsantner.markor:id/document__fragment__edit__content_editor__scrolling_parent").set_text("World")
        d(description="Navigate up").click()

    @precondition(
        lambda self: d(
            resourceId="net.gsantner.markor:id/fab_add_new_item"
        ).exists() and 
        d(resourceId="net.gsantner.markor:id/ui__filesystem_item__title").exists() and 
        int(d(resourceId="net.gsantner.markor:id/ui__filesystem_item__title").count) > 1 and
        d(resourceId="net.gsantner.markor:id/nav_notebook").info["selected"] and 
        d(resourceId="net.gsantner.markor:id/action_go_to").exists()
    )
    @rule()
    def view_file_should_exist_in_recent_viewed_documents(self):
        file_count = d(resourceId="net.gsantner.markor:id/ui__filesystem_item__title").count
        print("file count: "+str(file_count))
        if file_count == 0:
            print("no file to rename")
            return
        file_index = random.randint(0, file_count - 1)
        selected_file = d(resourceId="net.gsantner.markor:id/ui__filesystem_item__title")[file_index]
        file_name = selected_file.info['text']
        if "." not in file_name or ".." in file_name:
            print("not a file")
            return
        print("file name: "+str(file_name))
        selected_file.click()
        
        d(description="Navigate up").click()
        
        d(resourceId="net.gsantner.markor:id/action_go_to").click()
        
        d(text="Recently viewed documents").click()
        
        assert d(text=file_name).exists(), "file not in recently viewed documents"



if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/markor/2.8.0.apk",
        device_serial="emulator-5554",
        output_dir="../output/markor/1478/guided",
        policy_name="guided"
    )
    start_kea(t,setting)
    
