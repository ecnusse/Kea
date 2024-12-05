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

    @mainPath()
    def rule_go_back_mainpath(self):
        d(description="Navigate up").click()
        d(resourceId="com.amaze.filemanager:id/design_navigation_view").scroll(steps=10)
        d(text="Settings").click()
        d(scrollable = True).scroll.to(text="Back navigation")
        d(text="Back navigation").click()
        d.press("back")

    @precondition(lambda self: d(text="Go Back").exists() and 
                  d(resourceId="com.amaze.filemanager:id/second").exists() and 
                  d(resourceId="com.amaze.filemanager:id/fullpath").exists()
                  and d(resourceId="com.amaze.filemanager:id/fullpath").get_text() != ".."
                    )
    @rule()
    def rule_go_back(self):
        
        original_path = d(resourceId="com.amaze.filemanager:id/fullpath").get_text()
        print("original path: "+str(original_path))
        
        d(text="Go Back",resourceId="com.amaze.filemanager:id/secondLine").click()
        
        after_path = d(resourceId="com.amaze.filemanager:id/fullpath").get_text()
        print("after path: "+str(after_path))
        expected_path = '/'.join(original_path.split("/")[:-1])
        print("expected path: "+str(expected_path))
        assert after_path == expected_path



if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/amaze/amaze-3.3.0RC10.apk",
        device_serial="emulator-5554",
        output_dir="../output/amaze/1499/guided/1",
        policy_name="random",
    )
    start_kea(t,setting)
    
