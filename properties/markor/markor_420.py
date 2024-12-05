from kea.core import *

class Test(Kea):
    

    @initializer()
    def set_up(self):      
        if d(text="OK").exists():
            d(text="OK").click()

    @mainPath()
    def selection_should_discard_after_clicking_new_main_path(self):
        d(resourceId="net.gsantner.markor:id/fab_add_new_item").click()
        d(resourceId="net.gsantner.markor:id/note__activity__edit_note_title").set_text("Hello World!")
        d(resourceId="net.gsantner.markor:id/document__fragment__edit__content_editor__scrolling_parent").click()
        d.send_keys("hello")
        d(description="Navigate up").click()
        d(resourceId="net.gsantner.markor:id/note_title").long_click(duration=1)

    @precondition(lambda self: d(text="Select entries").exists() and 
                  d(resourceId="net.gsantner.markor:id/note_title").exists()
                  )
    @rule()
    def selection_should_discard_after_clicking_new(self):
        selected_info = d(resourceId="net.gsantner.markor:id/action_bar_subtitle").get_text()
        number_of_selected = selected_info.split(" ")[0]
        if number_of_selected == "One":
            number_of_selected = 1
        number_of_selected = int(number_of_selected)
        random.choice(d(resourceId="net.gsantner.markor:id/note_title")).click()
        
        if d(text="Select entries").exists():
            new_selected_info = d(resourceId="net.gsantner.markor:id/action_bar_subtitle").get_text()
            new_number_of_selected = new_selected_info.split(" ")[0]
            if new_number_of_selected == "One":
                new_number_of_selected = 1
            new_number_of_selected = int(new_number_of_selected)
            assert new_number_of_selected == number_of_selected - 1 or new_number_of_selected == number_of_selected + 1, "number of selected not correct"


if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/markor/1.3.0.apk",
        device_serial="emulator-5554",
        output_dir="../output/markor/420/guided",
        policy_name="guided"
    )
    start_kea(t,setting)
    
