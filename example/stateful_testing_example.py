import time

from kea.main import *
from kea.Bundle import Bundle

class Test2(Kea):
    _files = Kea.set_bundle("files")

    @initialize()
    def set_up(self):

        if d(text="ALLOW").exists():
            d(text="ALLOW").click()

    @precondition(lambda self: d(resourceId="com.amaze.filemanager:id/sd_main_fab").exists())
    @rule()
    def create_file_should_exist(self):
        d(resourceId="com.amaze.filemanager:id/sd_main_fab").click()
        d(resourceId="com.amaze.filemanager:id/sd_label", text="Folder").click()
        file_name = self._files.add_data()
        d.send_keys(file_name, clear=True)
        d(resourceId="com.amaze.filemanager:id/md_buttonDefaultPositive").click()
        d(scrollable=True).scroll.to(resourceId="com.amaze.filemanager:id/firstline", text=file_name)
        assert d(text=file_name).exists()

    @precondition(lambda self: self._files.get_all_data())
    @rule()
    def del_file_should_disappear(self):
        file_name = self._files.del_data()
        d(scrollable=True).scroll.to(resourceId="com.amaze.filemanager:id/firstline", text = file_name)
        selected_file = d(resourceId="com.amaze.filemanager:id/firstline", text = file_name)
        selected_file_name = selected_file.get_text()
        selected_file.right(resourceId="com.amaze.filemanager:id/properties").click()
        d(text="Delete").click()
        d(resourceId="com.amaze.filemanager:id/md_buttonDefaultPositive").click()
        assert not d(text=selected_file_name).exists()

    @precondition(lambda self: self._files.get_all_data())
    @rule()
    def change_filename_should_follow(self):
        file_name, new_name = self._files.change_filename()
        d(scrollable=True).scroll.to(resourceId="com.amaze.filemanager:id/firstline", text=file_name)
        selected_file = d(resourceId="com.amaze.filemanager:id/firstline", text=file_name)
        selected_file.right(resourceId="com.amaze.filemanager:id/properties").click()
        d(text="Rename").click()
        d.send_keys(new_name, clear=True)
        d(resourceId="com.amaze.filemanager:id/md_buttonDefaultPositive").click()
        d(scrollable=True).scroll.to(resourceId="com.amaze.filemanager:id/firstline", text=new_name)
        assert d(text=new_name).exists()
        d(scrollable=True).scroll.to(resourceId="com.amaze.filemanager:id/firstline", text=file_name)
        assert not d(text=file_name).exists()