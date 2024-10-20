import time

from kea.main import *
from kea.Bundle import Bundle

class Test2(Kea):
    _files = Kea.set_bundle("files")

    @initialize()
    def set_up(self):
        if d(text="Allow").exists():
            d(text="Allow").click()
        if d(text="GRANT").exists():
            d(text="GRANT").click()
        if d(text="ALLOW").exists():
            d(text="ALLOW").click()

    @precondition(lambda self: d(resourceId="com.amaze.filemanager:id/sd_main_fab").exists())
    @rule()
    def create_file_should_exist(self):
        d(resourceId="com.amaze.filemanager:id/pathbar").click()
        d(resourceId="com.amaze.filemanager:id/lin").child(index = 7).click()
        d(description="Navigate up").click()
        d(resourceId="com.amaze.filemanager:id/design_menu_item_text", textContains="Internal Storage").click()
        d(resourceId="com.amaze.filemanager:id/sd_main_fab").click()
        d(resourceId="com.amaze.filemanager:id/sd_label", text="Folder").click()
        file_name = self._files.get_random_test()
        d.send_keys(file_name, clear=True)
        d(resourceId="com.amaze.filemanager:id/md_buttonDefaultPositive").click()
        self._files.add(file_name)
        d(scrollable=True).scroll.to(resourceId="com.amaze.filemanager:id/firstline", text=file_name)
        assert d(text=file_name).exists()

    @precondition(lambda self: d(resourceId="com.amaze.filemanager:id/sd_main_fab").exists() and self._files.get_all_data())
    @rule()
    def del_file_should_disappear(self):
        d(resourceId="com.amaze.filemanager:id/pathbar").click()
        d(resourceId="com.amaze.filemanager:id/lin").child(index=7).click()
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
        d(resourceId="com.amaze.filemanager:id/pathbar").click()
        d(resourceId="com.amaze.filemanager:id/lin").child(index=7).click()
        d(scrollable=True).scroll.to(resourceId="com.amaze.filemanager:id/firstline", text=file_name)
        assert not d(text=selected_file_name).exists()

    @precondition(lambda self: d(resourceId="com.amaze.filemanager:id/sd_main_fab").exists() and self._files.get_all_data())
    @rule()
    def change_filename_should_follow(self):
        d(resourceId="com.amaze.filemanager:id/pathbar").click()
        d(resourceId="com.amaze.filemanager:id/lin").child(index=7).click()
        d(description="Navigate up").click()
        d(resourceId="com.amaze.filemanager:id/design_menu_item_text", textContains="Internal Storage").click()
        file_name = self._files.get_random_data()
        new_name = self._files.get_random_test()
        d(scrollable=True).scroll.to(resourceId="com.amaze.filemanager:id/firstline", text=file_name)
        selected_file = d(resourceId="com.amaze.filemanager:id/firstline", text=file_name)
        selected_file.right(resourceId="com.amaze.filemanager:id/properties").click()
        d(text="Rename").click()
        d.send_keys(new_name, clear=True)
        d(resourceId="com.amaze.filemanager:id/md_buttonDefaultPositive").click()
        self._files.update(file_name, new_name)
        d(resourceId="com.amaze.filemanager:id/pathbar").click()
        d(resourceId="com.amaze.filemanager:id/lin").child(index=7).click()
        d(scrollable=True).scroll.to(resourceId="com.amaze.filemanager:id/firstline", text=new_name)
        assert d(text=new_name).exists()
        d(resourceId="com.amaze.filemanager:id/pathbar").click()
        d(resourceId="com.amaze.filemanager:id/lin").child(index=7).click()
        d(scrollable=True).scroll.to(resourceId="com.amaze.filemanager:id/firstline", text=file_name)
        assert not d(text=file_name).exists()