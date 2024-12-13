from kea import *


class DelTest(KeaTest):
    _files = PublicBundle("files")

    @initializer()
    def set_up(self):
        if d(text="Allow").exists():
            d(text="Allow").click()
        if d(text="GRANT").exists():
            d(text="GRANT").click()
        if d(text="ALLOW").exists():
            d(text="ALLOW").click()


    @precondition(lambda self: self._files.get_all_data() and
                               d(resourceId="com.amaze.filemanager:id/sd_main_fab").exists() and
                               not d(resourceId="com.amaze.filemanager:id/action_mode_close_button").exists())
    @rule()
    def del_file_should_disappear(self):
        d.swipe_ext("down", scale=0.9)
        d(description="Navigate up").click()
        d(resourceId="com.amaze.filemanager:id/design_menu_item_text", textContains="Internal Storage").click()
        file_name = self._files.get_random_data()
        d(scrollable=True).scroll.to(resourceId="com.amaze.filemanager:id/firstline", text = file_name)
        selected_file = d(resourceId="com.amaze.filemanager:id/firstline", text = file_name)
        selected_file_name = selected_file.get_text()
        selected_file.right(resourceId="com.amaze.filemanager:id/properties").click()
        d(text="Delete").click()
        d(resourceId="com.amaze.filemanager:id/md_buttonDefaultPositive").click()
        self._files.delete(selected_file_name)
        d.swipe_ext("down", scale=0.9)
        d(resourceId="com.amaze.filemanager:id/home").click()
        d(scrollable=True).scroll.to(resourceId="com.amaze.filemanager:id/firstline", text=file_name)
        assert not d(text=selected_file_name).exists()

