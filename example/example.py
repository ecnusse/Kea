from kea.main import *

class Test1(Kea):

    @initialize()
    def pass_welcome_pages(self):
        for _ in range(5):
            d(resourceId="it.feio.android.omninotes.alpha:id/next").click()
        d(resourceId="it.feio.android.omninotes.alpha:id/done").click()

    @precondition(lambda self: d(resourceId="it.feio.android.omninotes.alpha:id/search_src_text").exists())
    @rule()
    def search_bar_should_exist_after_rotation(self):
        d.rotate('l')
        d.rotate('n')
        assert d(resourceId="it.feio.android.omninotes.alpha:id/search_src_text").exists()