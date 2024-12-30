创建并运行模拟器
=======================================

在运行 Kea 之前，你需要创建一个模拟器。有关如何使用 `avdmanager <https://developer.android.com/studio/command-line/avdmanager>`_ 创建 avd 的信息，请参见 `此链接 <https://stackoverflow.com/questions/43275238/how-to-set-system-images-path-when-creating-an-android-avd>`_。
以下示例命令将帮助你创建一个模拟器，从而快速开始使用 Kea：

.. code-block:: console

    sdkmanager "build-tools;29.0.3" "platform-tools" "platforms;android-29"
    sdkmanager "system-images;android-29;google_apis;x86"
    avdmanager create avd --force --name Android10.0 --package 'system-images;android-29;google_apis;x86' --abi google_apis/x86 --sdcard 1024M --device "pixel_2"


接下来，你可以使用以下命令启动一个模拟器并分配其端口号：

.. code-block:: console

    emulator -avd Android10.0 -read-only -port 5554
