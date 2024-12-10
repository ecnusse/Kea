from kea import *

class HarmonyOS_example(KeaTest):

    @precondition(lambda self: d(text="家具厨具").exists())
    @rule()
    def DaiFuKuan_exists_when_in_WoDe(self):
        d(text="我的").click()
        assert d(text="待付款").exists()