.. _pdl_api:

PDL API 
=================

PDL for Property Description Language. This is how kea interact with AUT(App under test).

UI events
-----------------

.. note::

   Currently, kea uses `uiautomator2 <https://github.com/openatx/uiautomator2>`_ to interact with the app.
   You can find more information in `uiautomator2 <https://github.com/openatx/uiautomator2>`_.
   You can also use other tools to interact with the app, which can be easily implemented by modifying the `dsl.py`.

For example, to send the click event to the app, you can use the following code:

.. code-block:: Python

   d(resourceId="player_playback_button").click()


``d`` is the object of the uiautomator2.
``resourceId`` sets the resource id of the element.
``click()`` sends the click event to the element.

Here are some common operations:

* click

   .. code-block:: Python

      d(text="OK").click()
  
* long_click

   .. code-block:: Python

      d(text="OK").long_click()

* edit text

   .. code-block:: Python

      d(text="OK").set_text("text")

* rotate device

   .. code-block:: Python

      d.rotate("l") # or left
      d.rotate("r") # or right

* press [key]

   .. code-block:: Python

      d.press("home")
      d.press("back")

You can use selector to identify the UI object in the current window.

Selector 
---------------------

you can also look at `uiautomator2 Selector <https://github.com/openatx/uiautomator2?tab=readme-ov-file#selector>`_.
Selector is a handy mechanism to identify a specific UI object in the current window.  
Selector supports below parameters.

*  `text`, `textContains`, `textMatches`, `textStartsWith`
*  `className`, `classNameMatches`
*  `description`, `descriptionContains`, `descriptionMatches`, `descriptionStartsWith`
*  `checkable`, `checked`, `clickable`, `longClickable`
*  `scrollable`, `enabled`,`focusable`, `focused`, `selected`
*  `packageName`, `packageNameMatches`
*  `resourceId`, `resourceIdMatches`
*  `index`, `instance`  


Examples
---------------------------

Here are some examples.

.. code-block:: python

   # Select the widget that has text "More Options" and click it.
   d(text='More Options').click()

   # Use multiple fields in one selector.
   # Select the widget that has text "Clock" and className "android.widget.TextView" and click it.
   d(text='Clock', className='android.widget.TextView').long_click()

   # Select the widget that has resourceId "com.example/input_box" and set its text to "Hello world"
   d(resourceId="com.example/input_box").set_text("Hello world")
