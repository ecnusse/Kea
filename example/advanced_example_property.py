import sys

sys.path.append("..")
from kea.core import *


class Test(Kea):

    @initializer()
    def set_up(self):
        d.set_fastinput_ime(True)
        d(resourceId="it.feio.android.omninotes:id/next").click()

        d(resourceId="it.feio.android.omninotes:id/next").click()

        d(resourceId="it.feio.android.omninotes:id/next").click()

        d(resourceId="it.feio.android.omninotes:id/next").click()

        d(resourceId="it.feio.android.omninotes:id/next").click()

        d(resourceId="it.feio.android.omninotes:id/done").click()

        if d(text="OK").exists():
            d(text="OK").click()

    @mainPath()
    def remove_password_in_setting_should_effect_mainpath(self):
        d(resourceId="it.feio.android.omninotes:id/fab_expand_menu_button").long_click()
        d(resourceId="it.feio.android.omninotes:id/detail_content").set_text("Hello world")
        d(description="More options").click()
        d(text="Lock").click()
        d(resourceId="it.feio.android.omninotes:id/password").set_text("1")
        d(resourceId="it.feio.android.omninotes:id/password_check").set_text("1")
        d(resourceId="it.feio.android.omninotes:id/question").set_text("1")
        d(resourceId="it.feio.android.omninotes:id/answer").set_text("1")
        d(resourceId="it.feio.android.omninotes:id/answer_check").set_text("1")
        d(scrollable=True).scroll.to(text="OK")
        d(text="OK").click()
        d.press("back")
        d(description="drawer open").click()
        d(resourceId="it.feio.android.omninotes:id/settings").click()
        d(resourceId="android:id/title", text="Data").click()
        d(resourceId="android:id/title", text="Password").click()
        d(resourceId="it.feio.android.omninotes:id/password_remove").click()

    @precondition(lambda self: d(text="Insert password").exists() and d(text="PASSWORD FORGOTTEN").exists())
    @rule()
    def remove_password_in_setting_should_effect(self):

        d(resourceId="it.feio.android.omninotes:id/customViewFrame").click()

        d.send_keys("1", clear=True)

        d(resourceId="it.feio.android.omninotes:id/buttonDefaultPositive").click()

        if d(text="Insert password").exists():
            print("wrong password")
            return

        d(resourceId="it.feio.android.omninotes:id/buttonDefaultPositive").click()

        d.press("back")

        d.press("back")

        d.press("back")

        d.press("back")

        assert not d(resourceId="it.feio.android.omninotes:id/lockedIcon").exists()



