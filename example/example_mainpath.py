from kea.main import *


class Test(Kea):

    @initialize()
    def set_up(self):
        for _ in range(5):
            d(resourceId="it.feio.android.omninotes.alpha:id/next").click()
        d(resourceId="it.feio.android.omninotes.alpha:id/done").click()

    @main_path()
    def test_main(self):
        d(resourceId="it.feio.android.omninotes.alpha:id/fab_expand_menu_button").long_click()
        d(resourceId="it.feio.android.omninotes.alpha:id/detail_content").click()
        d.send_keys("read a book #Tag1", clear=True)
        d(description="drawer open").click()

    @precondition(lambda self: d(resourceId="it.feio.android.omninotes.alpha:id/menu_tag").exists() and
                               "#" in d(resourceId="it.feio.android.omninotes.alpha:id/detail_content").info["text"]
                  )
    @rule()
    def rule_remove_tag_from_note_shouldnot_affect_content(self):
        # get the text from the note's content
        origin_content = d(resourceId="it.feio.android.omninotes.alpha:id/detail_content").info["text"]
        # click to open the tag list
        d(resourceId="it.feio.android.omninotes.alpha:id/menu_tag").click()
        # select a tag to remove
        selected_tag = random.choice(d(className="android.widget.CheckBox", checked=True))
        select_tag_name = "#" + \
                          selected_tag.right(resourceId="it.feio.android.omninotes.alpha:id/md_title").info["text"].split(
                              " ")[0]
        selected_tag.click()
        # click to uncheck the selected tag
        d(text="OK").click()
        # get the updated content after removing the tag
        new_content = d(resourceId="it.feio.android.omninotes.alpha:id/detail_content").info["text"].strip().replace(
            "Content", "")
        # get the expected content after removing the tag
        origin_content_exlude_tag = origin_content.replace(select_tag_name, "").strip()
        # the tag should be removed in the content and the updated content should be the same as the expected content
        assert not d(textContains=select_tag_name).exists() and new_content == origin_content_exlude_tag