Set up HarmonyOS environment
=======================================

.. tip:: 

   What you need to do in this chapter:

   **1. Make the `hdc` cmd available**
   
   Kea for relies on ``hdc`` cmd to interact with android devices. The key is to make the HDC
   cmd available by adding it into PATH var.

   **2. Connect a device or start an emulator on your PC**


1. Install DevEco Studio
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Download and install DevEco Stuido: `Download DevEco Stuido <https://developer.huawei.com/consumer/cn/deveco-studio/>`_.


2. Set up cmdline tools (hdc)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Open DevEco Studio. Go to :guilabel:`DevEco Studio` -> :guilabel:`preferences` -> :guilabel:`OpenHarmony SDK`.

.. figure:: ../../images/DevEco-sdk.jpg
   :align: center

   sdk setting in DevEco Studio

Click :guilabel:`edit`. Set your sdk path and install the openharmony SDK - toolchains. **The api version should be 12+ (5.0+).**

.. figure::  ../../images/DevEco-toolchains.jpg
   :align: center

   Download toolchains (API 12+)

Export the path to your system. If you have problem setting up your environment vars,
you can checkout :ref:`path_setup` for details.

.. code-block:: bash

   # macOS and Linux
   HARMONY_SDK_HOME="<Your path to opensdk home>"
   export PATH="$HARMONY_SDK_HOME/12/toolchains"

   # Windows
   HARMONY_SDK_HOME: "<Your path to opensdk home>"
   PATH: %HARMONY_SDK_HOME%\12\toolchains

.. important::
    Enter ``hdc`` in your terminal to check if the setup succeed.


3. Run an emulator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Checkout `Manage and run HarmonyOS emulator <https://developer.huawei.com/consumer/cn/doc/harmonyos-guides-V13/ide-emulator-management-V13>`_ to run an emulator.

.. important::
    Enter ``hdc list targets`` in your terminal. You should see your emulator listed in a loopback address form.
