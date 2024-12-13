from kea import *


class CreateTest(KeaTest):
    _files = PublicBundle("files")

    @initializer()
    def set_up(self):
        if d(text="Allow").exists():
            d(text="Allow").click()
        if d(text="GRANT").exists():
            d(text="GRANT").click()
        if d(text="ALLOW").exists():
            d(text="ALLOW").click()


    @precondition(lambda self: d(resourceId="com.amaze.filemanager:id/sd_main_fab").exists() and
                               not d(textContains = "SDCARD").exists())
    @rule()
    def create_file_should_exist(self):
        d.swipe_ext("down", scale=0.9)
        d(description="Navigate up").click()
        d(resourceId="com.amaze.filemanager:id/design_menu_item_text", textContains="Internal Storage").click()
        d(resourceId="com.amaze.filemanager:id/sd_main_fab").click()
        d(resourceId="com.amaze.filemanager:id/sd_label", text="Folder").click()
        file_name = self._files.get_random_value()
        d.send_keys(file_name, clear=True)
        d(resourceId="com.amaze.filemanager:id/md_buttonDefaultPositive").click()
        self._files.add(file_name)
        d(scrollable=True).scroll.to(resourceId="com.amaze.filemanager:id/firstline", text=file_name)
        assert d(text=file_name).exists()
