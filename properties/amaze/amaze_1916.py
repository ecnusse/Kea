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
            
    @mainPath()
    def rule_documnets_mainpath(self):
        d(description="Navigate up").click()
        d(resourceId="com.amaze.filemanager:id/design_navigation_view").scroll(steps=10)
        d(text="Documents").click()

    @precondition(lambda self: d(text="Documents").exists()  and not d(text="Settings").exists())
    @rule()
    def rule_documnets(self):
        
        
        assert d(resourceId="com.amaze.filemanager:id/firstline").exists()



if __name__ == "__main__":
    t = Test()
    
    setting = Setting(
        apk_path="./apk/amaze/amaze-3.4.3.apk",
        device_serial="emulator-5554",
        output_dir="../output/amaze/1916/guided/1",
        policy_name="random"
    )
    start_kea(t,setting)
    
