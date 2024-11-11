from kea.main import *

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
    def create_file_with_same_name_should_not_overwrite_mainpath(self):
        d(resourceId="net.gsantner.markor:id/fab_add_new_item").click()
        d(resourceId="net.gsantner.markor:id/new_file_dialog__name").set_text("Hello World")
        d(text="OK").click()
        d(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").set_text("Hello World!!!")
        d(description="Navigate up").click()

    @precondition(
        lambda self: d(resourceId="net.gsantner.markor:id/ui__filesystem_item__title").exists() and
        d(resourceId="net.gsantner.markor:id/ui__filesystem_item__title").count >= 2 and 
        d(resourceId="net.gsantner.markor:id/fab_add_new_item").exists() and not 
        d(text="Settings").exists() and not 
        d(text="Date").exists() and not 
        d(resourceId="net.gsantner.markor:id/action_rename_selected_item").exists()
        )
    @rule()
    def create_file_with_same_name_should_not_overwrite(self):
        file_count = d(resourceId="net.gsantner.markor:id/ui__filesystem_item__title").count
        print("file count: "+str(file_count))
        if file_count == 0:
            print("no file ")
            return
        file_index = random.randint(0, file_count - 1)
        selected_file = d(resourceId="net.gsantner.markor:id/ui__filesystem_item__title")[file_index]
        file_name = selected_file.info['text']
        file_name_suffix = file_name.split(".")[-1]
        file_name_prefix = file_name.split(".")[0]
        if "." not in file_name or ".." in file_name:
            print("not a file")
            return
        print("file name: "+str(file_name))
        selected_file.click()
        
        original_content = d(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").get_text()
        print("original content: "+str(original_content))
        d(description="Navigate up").click()
        
        d(resourceId="net.gsantner.markor:id/fab_add_new_item").click()
        
        d(resourceId="net.gsantner.markor:id/new_file_dialog__name").set_text(file_name_prefix)
        d(resourceId="net.gsantner.markor:id/new_file_dialog__ext").set_text("."+file_name_suffix)
        
        d(text="OK").click()
        
        new_content = d(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").get_text()
        print("new content: "+str(new_content))
        assert original_content == new_content, "create file with same name should not overwrite"


if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/markor/2.2.10.apk",
        device_serial="emulator-5554",
        output_dir="../output/markor/994/mutate",
        policy_name="mutate"
    )
    start_kea(t,setting)
    
