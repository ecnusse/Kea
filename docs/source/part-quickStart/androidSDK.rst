Set up Android Environment
========================================

Follow these steps to install AndroidSDK on different Operating System.

.. tip:: 

   What you need to do (also the target of this chapter) before using kea:

   **1. Make the `adb` cmd available**
   
   Kea relies on ``adb`` cmd to interact with android devices. The key is to make the ADB(Android Debug Bridge) 
   cmd available by adding it into PATH var.

   **2. Connect a device or start an emulator on your PC**


:guilabel:`Option A` Setup your environment with Android Studio
---------------------------------------------------------------------
:doc:`androidStudio_setup/Android_Studio`

.. toctree::
   :hidden:

   androidStudio_setup/Android_Studio




:guilabel:`Option B` Setup your environment with cmds
-------------------------------------------------------------------

**Step 1: Install and set up android sdk on your PC**

:doc:`androidSDK/Linux`

:doc:`androidSDK/Windows`

:doc:`androidSDK/Mac`

**Setp 2: Create and run an emulator**

:doc:`androidSDK/emulator`

.. toctree::
   :hidden:
   
   androidSDK/Linux
   androidSDK/Windows
   androidSDK/Mac
   androidSDK/emulator
