Write your first property
======================================

Check your Environment
--------------------------------------
Kea is a property based testing framework for mobile apps. Support Andorid and HarmonyOS now.

Make sure you have a mobile device and android/harmonyOS cmdline tools installed on your PC. Check if the ``adb`` (Andorid) or ``hdc`` (HarmonyOS) is available.

If you don't have a device. You can try Kea with an emulator.

Make sure you have ``python 3.9+``.

Installation
--------------------------------------
To install Kea, use:

.. code-block:: console

    git clone https://github.com/ecnusse/Kea.git
    cd Kea
    pip install -e .

Enter ``kea -h`` to check whether kea has been successfully installed.

Write your first property
--------------------------------------

Start your device or android emulator. Enter ``adb devices`` in your terminal to make sure it's available.

we will use `weditor <https://github.com/alibaba/web-editor>`_ to inspect android elements and write property.

**1. Launch weditor and install your app.**

.. code-block:: bash 

    pip install weditor==0.7.3
    python -m weditor

The above command will install weditor on your PC and start weditor. It offers a host server (default: http://localhost:17310). You can access it in your web browser.

.. figure:: ../../images/weditor_home.png
    :align: center

    The home page of weditor.

Then, cd into the kea workspace and install the app omninotes.

.. code-block:: bash

    adb install example/omninotes.apk

Check if the app has been installed successfully.

**2. Dump hierachy and inspect android elements**

Dump the hierachy in weditor to get android elements.

:guilabel:`Enter Device serial` -> :guilabel:`Connect` -> :guilabel:`Dump Hierachy`

.. figure:: ../../images/weditor-usage2.png
    :align: center

    Dump hierachy from weditor

Once connected to the weditor. You can click :guilabel:`Dump Hierachy` to refresh the elements (aka. dump hierachy) every time your screen changes.
Or you can enable the automatic dump hierachy to avoid manuelly refresh the elements.

You can click an element and inspect its attributes.

**3. Write your first property**

We have a simple function to check in this app: **The search input box should not be cleared after rotation.** 

Now, let's write the precondition. This should be a unique feature in the start of the function. We want to check the search input box, so let's 
move to the search function first. By clicking the :guilabel:`search` button, you can enter the search edit page. Obviously, the unique feature of this
page should be the search input box itself.

**Dump hierachy in weditor. Click the search box to inspect its attributes.**

.. figure:: ../../images/weditor-prop1.png
    :align: center

    Inspect a widget in weditor

We need the widget-specific attr to target a widget. The most commonly used unique attr is **resourceId**. 
if you don't have a **resourceId**, **text** or **className** 
also works, but most of time they are not unique and will lead to mistake. 

So, in order to avoid kea running into wrong states, you can target a widget with multiple attrs in Selector and target a page with multiple
widgets.

**After inspection, we know the resourceId of search input box. We can target it with the following command.**

``d(resourceId="it.feio.android.omninotes.alpha:id/search_src_text")``

.. note:: 

    You may be confused by the ``d(**Selector)`` script. This is kea's PDL(Property description Languague) 
    for interacting with AUT(App under test). You can read :ref:`pdl_api` for details.

**To check whether this widget exist, we call the method ``exists``.**

``d(resourceId="it.feio.android.omninotes.alpha:id/search_src_text").exists()``


.. hint:: 
    Double click the widget in weditor. This will automatically generate the **click** action script for 
    you. You can take reference from it to write your own script.

**Write the interaction scenerio (aka. what does the function do).**

We need to rotate the device. From neutural to landscape and back to neutural. The script can be written like.
``d.rotate('l')``
``d.rotate('n')``

**Write the post conditon. The inputbox should still exist after the rotation. We use an assertion to confirm its existance.**

``assert d(resourceId="it.feio.android.omninotes.alpha:id/search_src_text").exists()``

That's it! You've already wrote your first property!

**4. Encapsule your property with Kea APIs**

Create a python file **my_prop.py** under kea's root directory.

.. code-block:: python

    #my_prop.py
    from kea.core import *

    class CheckSearchBox(Kea):
        @precondition(lambda self: d(resourceId="it.feio.android.omninotes.alpha:id/search_src_text").exists())
        @rule()
        def search_box_should_exist_after_rotation(self):
            d.rotate('l')
            d.rotate('n')
            assert d(resourceId="it.feio.android.omninotes.alpha:id/search_src_text").exists()
    

Start kea and check your property
--------------------------------------


Start kea by the following command.

.. code-block:: bash

    kea -f prop.py -a example/omninotes.apk -o output

Check the bug report in ``output/bug_report.html``. You can learn to read bug report in this
tutorial: :ref:`bug_report_tutorial`.