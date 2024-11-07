from kea.main import *

class Test(Kea):
    

    @initialize()
    def set_up(self):
        if d(text="OK").exists():
            d(text="OK").click()
    
    # bug #457
    @precondition(lambda self: d(resourceId="net.gsantner.markor:id/nav_notebook").exists())
    @rule()
    def swipe_should_update_title(self):
        # d.swipe_ext("left")
        if d(resourceId="net.gsantner.markor:id/nav_todo").info["selected"]:
            assert  d(resourceId="net.gsantner.markor:id/toolbar").child(text="To-Do").exists(), "To-Do not exists"
        elif d(resourceId="net.gsantner.markor:id/nav_quicknote").info["selected"]:
            assert  d(resourceId="net.gsantner.markor:id/toolbar").child(text="QuickNote").exists(), "QuickNote not exists"
        elif d(resourceId="net.gsantner.markor:id/nav_more").info["selected"]:
            assert  d(resourceId="net.gsantner.markor:id/toolbar").child(text="More").exists(),   "More not exists"
        elif d(resourceId="net.gsantner.markor:id/nav_notebook").info["selected"]:
            assert  d(resourceId="net.gsantner.markor:id/toolbar").child(text="Markor").exists(), "Markor not exists"



t = Test()

setting = Setting(
    apk_path="./apk/markor/1.5.1.apk",
    device_serial="emulator-5554",
    output_dir="../output/markor/457/mutate",
    policy_name="mutate"
)
start_kea(t,setting)

