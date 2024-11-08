from kea.main import *

class Test(Kea):
    

    @initializer()
    def set_up(self):
        d(resourceId="net.gsantner.markor:id/next").click()
        
        d(resourceId="net.gsantner.markor:id/next").click()
        
        d(resourceId="net.gsantner.markor:id/next").click()
        
        d(resourceId="net.gsantner.markor:id/next").click()
        
        d(text="DONE").click()
        
        
        if d(text="OK").exists():
            d(text="OK").click()

    @mainPath()
    def rotation_should_keep_view_mode_mainpath(self):
        d(resourceId="net.gsantner.markor:id/fab_add_new_item").click()
        d(resourceId="net.gsantner.markor:id/new_file_dialog__name").set_text("Hello World!")
        d(text="OK").click()
        d(resourceId="net.gsantner.markor:id/action_preview").click()

    # 1137
    @precondition(
        lambda self: d(resourceId="net.gsantner.markor:id/action_edit").exists()
        )
    @rule()
    def rotation_should_keep_view_mode(self):
        d.set_orientation("l")
        
        d.set_orientation("n")
        
        assert d(resourceId="net.gsantner.markor:id/action_edit").exists()




t = Test()

setting = Setting(
    apk_path="./apk/markor/2.11.1.apk",
    device_serial="emulator-5554",
    output_dir="../output/markor/1137/mutate_new",
    policy_name="mutate"
)
start_kea(t,setting)

