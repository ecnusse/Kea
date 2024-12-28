How to write properties
================================

In this tutorial, you will learn how to write properties and test them with Kea.

In mobile apps, a property defines the expected behavior of the app. 
Then, if the app violates the property, it means a bug is found.

At high level, a property consists of three key components **<P, I, Q>**, where (1) *P* is a precondition, 
(2) *I* is an interaction scenario which defines how to perform the app functionality, 
and (3) *Q* is a postcondition which defines the expected behavior.

Kea uses ``@initializer()`` to pass the welcome page or the login page of the app.

In Kea, a property is defined by applying the ``@rule()`` decorator on a function.

To define the precondition of the property, you can use the ``@precondition()`` decorator on the  ``@rule()``-decorated function.

The postcondition is defined by the ``assert`` statement in the ``@rule()``-decorated function.

For mobile apps, you may can get properties from multiple sources, such as the app's specification, the app's documentation, the app's test cases, the app's bug reports, etc.

Let's start with a simple example on how to get a property, write the property in Kea, and test the property by Kea.

Specify property from historical bugs
---------------------------------------------

This example will show how to get a property from the app `OmniNotes <https://github.com/federicoiosue/Omni-Notes/>`_

`OmniNotes <https://github.com/federicoiosue/Omni-Notes/>`_ is an app for taking and managing notes.

Here is a bug report from the app `#634 <https://github.com/federicoiosue/Omni-Notes/issues/634>`_, where a user complained that when he removed a tag, it removed other tags that sharing the same prefix.

Then, from this bug report, you can get a property:

After removing the tag, the tag should be successfully removed and the note content should remain unchanged.

From the bug report, you can get a property as follows:

- **P (Precondition)**: The tag exists.
- **I (Interaction scenario)**: Remove the note tag from the tag list.
- **Q (Postcondition)**: The tag is removed and the note content remains unchanged.

Let's write the property in Kea.


.. code-block:: Python

    @precondition(lambda self: d(resourceId="it.feio.android.omninotes:id/menu_tag").exists() and
                   "#" in d(resourceId="it.feio.android.omninotes:id/detail_content").info["text"]
                   )
    @rule()
    def rule_remove_tag_from_note_shouldnot_affect_content(self):
        # get the text from the note's content
        origin_content = d(resourceId="it.feio.android.omninotes:id/detail_content").info["text"]
        # click to open the tag list
        d(resourceId="it.feio.android.omninotes:id/menu_tag").click()
        # select a tag to remove
        selected_tag = random.choice(d(className="android.widget.CheckBox",checked=True))
        select_tag_name = "#"+ selected_tag.right(resourceId="it.feio.android.omninotes:id/md_title").info["text"].split(" ")[0]
        selected_tag.click()
        # click to uncheck the selected tag
        d(text="OK").click()
        # get the updated content after removing the tag
        new_content = d(resourceId="it.feio.android.omninotes:id/detail_content").info["text"].strip().replace("Content", "")
        # get the expected content after removing the tag
        origin_content_exlude_tag = origin_content.replace(select_tag_name, "").strip()
        # the tag should be removed in the content and the updated content should be the same as the expected content
        assert not d(textContains=select_tag_name).exists() and new_content == origin_content_exlude_tag

The ``@precondition`` decorator defines when the property should be tested.
Here, ``d(resourceId="it.feio.android.omninotes:id/menu_tag").exists()`` checks if the tag button exists and 
``"#" in d(resourceId="it.feio.android.omninotes:id/detail_content").info["text"]`` checks if the note content contains a tag. 


The ``@rule()`` decorator defines the property.
Here, the interaction scenario is to remove a tag.

The postcondition is defined by the ``assert`` statement.
Here, Kea checks if the tag is removed and content remains unchanged.

That's it! This is a property that should be held by `OmniNotes <https://github.com/federicoiosue/Omni-Notes/>`_.

Also, you can add a function to set up the app's initial state before testing the property.

To do this, you can use ``@initializer()`` to specify a function and write the corresponding UI events to pass the welcome page:

.. code:: Python

    @initializer()
    def set_up(self):
        for _ in range(5):
            d(resourceId="it.feio.android.omninotes:id/next").click()
        d(resourceId="it.feio.android.omninotes:id/done").click()
        if d(text="OK").exists():
            d(text="OK").click()

Here, the code can automatically pass the welcome page in `OmniNotes <https://github.com/federicoiosue/Omni-Notes/>`_.
Note that you can use the ``@initializer()`` decorator to define the setup function.
Then, Kea will execute the setup function before testing the property.

.. note::

    This feature can be used to set up the app's initial state before testing the property. 
    For example, use this feature to pass the login, add data to the app, etc.
    If you don't need to set up the app's initial state, you can skip it.

Moreover, if you want to use the main path guided exploration strategy, you should set a main path function.

To do this, you can use the following code:

.. code:: Python

    @mainPath()
    def test_main(self):
        d(resourceId="it.feio.android.omninotes:id/fab_expand_menu_button").long_click()
        d(resourceId="it.feio.android.omninotes:id/detail_content").click()
        d(resourceId="it.feio.android.omninotes:id/detail_content").set_text("read a book #Tag1")
        d(description="drawer open").click()
        d(resourceId="it.feio.android.omninotes:id/note_content").click()
        d(resourceId="it.feio.android.omninotes:id/menu_tag").click()
        d(resourceId="it.feio.android.omninotes:id/md_control").click()
        d(resourceId="it.feio.android.omninotes:id/md_buttonDefaultPositive").click()

The code above can guide Kea to create a note with the content of "read a book #Tag1" in the omninotes.
And then removes the tag “Tag1” of this note.

.. note::

    In the part of the definition of the main path, you can only use UI operation commands to complete the definition;
    The function cannot contain other Python statements such as for loops.
    But we believe this approach is sufficient to implement the functionality of the main path.

Here, you have already learned how to write a property in Kea.

To test this property, you need to put the property in a class, which inherits from the ``Kea`` class.

.. code:: Python
    
    from kea.main import *

    class Test(Kea):
        

        @initialize()
        def set_up(self):
            for _ in range(5):
                d(resourceId="it.feio.android.omninotes:id/next").click()
            d(resourceId="it.feio.android.omninotes:id/done").click()
            if d(text="OK").exists():
                d(text="OK").click()

        @mainPath()
        def test_main(self):
            d(resourceId="it.feio.android.omninotes:id/fab_expand_menu_button").long_click()
            d(resourceId="it.feio.android.omninotes:id/detail_content").click()
            d(resourceId="it.feio.android.omninotes:id/detail_content").set_text("read a book #Tag1")
            d(description="drawer open").click()
            d(resourceId="it.feio.android.omninotes:id/note_content").click()
            d(resourceId="it.feio.android.omninotes:id/menu_tag").click()
            d(resourceId="it.feio.android.omninotes:id/md_control").click()
            d(resourceId="it.feio.android.omninotes:id/md_buttonDefaultPositive").click()

        @precondition(lambda self: d(resourceId="it.feio.android.omninotes:id/menu_tag").exists() and
                    "#" in d(resourceId="it.feio.android.omninotes:id/detail_content").info["text"]
                    )
        @rule()
        def rule_remove_tag_from_note_shouldnot_affect_content(self):
            # get the text from the note's content
            origin_content = d(resourceId="it.feio.android.omninotes:id/detail_content").info["text"]
            # click to open the tag list
            d(resourceId="it.feio.android.omninotes:id/menu_tag").click()
            # select a tag to remove
            selected_tag = random.choice(d(className="android.widget.CheckBox",checked=True))
            select_tag_name = "#"+ selected_tag.right(resourceId="it.feio.android.omninotes:id/md_title").info["text"].split(" ")[0]
            selected_tag.click()
            # click to uncheck the selected tag
            d(text="OK").click()
            # get the updated content after removing the tag
            new_content = d(resourceId="it.feio.android.omninotes:id/detail_content").info["text"].strip().replace("Content", "")
            # get the expected content after removing the tag
            origin_content_exlude_tag = origin_content.replace(select_tag_name, "").strip()
            # the tag should be removed in the content and the updated content should be the same as the expected content
            assert not d(textContains=select_tag_name).exists() and new_content == origin_content_exlude_tag

Here, you need to write the property in the ``Test`` class, which inherits from the ``Kea`` class.

We put this file example_mainpath_property.py in the ``example`` directory.
You can test the property by running the following command:

.. code:: console

    kea -f example/example_mainpath_property.py -a example/omninotes.apk

When you try to test this property, you may quickly find two new bugs that violates this property.
Then, you can write the corresponding bug reports and submit them to the app's developers.
Both of them are fixed by app developers.

You can see the bug reports:

1. `Bug Report: Note tag cannot be removed <https://github.com/federicoiosue/Omni-Notes/issues/942>`_.


2. `Bug Report: Deleting One Tag in a Note Affects Another Tag in the Same Note <https://github.com/federicoiosue/Omni-Notes/issues/949>`_.

Specify property from app function
---------------------------------------------
This example will show how to get a property from the app `OmniNotes <https://github.com/federicoiosue/Omni-Notes/>`_

`OmniNotes <https://github.com/federicoiosue/Omni-Notes/>`_ is an app for taking and managing notes.

In the settings of Omninotes, there is a function that can set or remove a lock for a note. So you may can define a property
``remove_password_in_setting_should_effect``. Just means when you remove a lock in the settings, the note must unlocked.

To do this, first you should use ``@initializer()`` to specify a function and write the corresponding UI events to pass the welcome page:

.. code:: Python

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

Then you can define a function as the main path guide the app to lock a note and jump to the remove lock interface, just like this:

.. code:: Python

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

The most important thing is define the property, you should use ``@rule()`` and ``@precondition()`` to finish it. Here, the precondition
*P* is use two UI components to check whether the app is in the remove lock interface. And then execute some events to remove the lock.
Finally, check whether the locked note becomes unlocked.

.. code:: Python

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

We put this file advanced_example_property.py in the ``example`` directory.
You can test the property by running the following command:

.. code:: console

    kea -f example/advanced_example_property.py -a example/omninotes-5.5.3.apk


That's it! You have learned how to write a property and test it with Kea.

.. note::

    You can write a property or some properties in one ``.py`` file as one TestCase, of course, you can also write multiple properties in multiple ``.py`` files.
    But if you choose the first method you should make sure there is at most one ``@initializer()`` and at most one ``@mainPath()`` in a ``.py`` file, but
    you can have multiple ``@rule()`` and ``@precondition()``. The structure of TestCase is in the image below.

.. image:: ../../images/TestCase.png
            :align: center

|