.. _android_studio_env:

使用安卓模拟器配置安卓环境
========================================================


.. important:: 
    **前提条件：** 在你的电脑上安装 Android Studio。

    你可以在 https://developer.android.com/studio 下载 Android Studio。

.. hint:: 
    Kea 依赖 ``adb`` 命令与 Android 设备进行交互。关键是要确保 ADB（Android 调试桥）命令可用。
    以下教程将帮助你设置整个 Android SDK 工具套件。但请记住，将 ``adb`` 命令添加到路径中就足够了。

.. _path_setup:

1. 设置命令行工具（adb）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

MacOS 和 Linux
-------------------------------

在你的电脑上安装了 Android Studio。你需要做的是将 Android sdk 其添加至 PATH 环境变量，让其在终端中生效。

有关详细信息，请参见 `Android Studio 文档：环境变量 <https://developer.android.com/tools/variables>`_。

如果你使用的是 zsh 或 bash，请使用 ``EXPORT`` 命令设置 ``ANDROID_HOME`` 环境变量。``ANDROID_HOME`` 
环境变量应指向你的 SDK 安装路径。默认路径是 ``/usr/Library/Android/sdk/``。你可以通过 :guilabel:`Android Studio` -> :guilabel:`设置` -> :guilabel:`语言与框架` -> :guilabel:`Android SDK` 查看你的安装路径。

在此窗口中，查看 :guilabel:`SDK 工具`，安装 **Android SDK 平台工具**。

.. figure:: ../../../images/android_home_path.jpg
    :align: center

    Android Studio 中 Android SDK 路径的示例

然后，将路径添加到 .bashrc 或 .zshrc 文件中。

.. code-block:: bash

    export ANDROID_HOME="/usr/.../Library/Android/sdk/"
    # export 安卓安装目录中的所有命令。
    export PATH="$ANDROID_HOME/emulator:$ANDROID_HOME/tools:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/tools/bin:$ANDROID_HOME/cmdline-tools/latest:$ANDROID_HOME/platform-tools:$PATH"


``source`` shell的配置文件以激活修改。

.. important:: text

    在终端中输入 ``adb`` 检查设置是否成功。

Windows
---------------

在你的电脑上安装了 Android Studio。你需要做的是将 Android sdk 其添加至 PATH 环境变量，让其在终端中生效。

如果你使用的是 zsh 或 bash，请使用 ``EXPORT`` 命令设置 ``ANDROID_HOME`` 环境变量。``ANDROID_HOME`` 
环境变量应指向你的 SDK 安装路径。默认路径是 ``C:\Users\usr_name\AppData\Local\Android\Sdk``。你可以通过 :guilabel:`文件` -> :guilabel:`设置` -> :guilabel:`语言与框架` -> :guilabel:`Android SDK` 查看你的安装路径。

在此窗口中，查看 :guilabel:`SDK 工具`，安装 **Android SDK 平台工具**。

.. figure:: ../../../images/android_home_path_win.png
    :align: center

    Android Studio 中 Android SDK 路径的示例

然后，将以下路径添加到 PATH 变量中。请参见 `Windows系统中如何添加 PATH 环境变量 <https://helpdeskgeek.com/windows-10/add-windows-path-environment-variable/>`_。

.. code-block:: 

    ANDROID_HOME:
    C:\Users\usr_name\AppData\Local\Android\Sdk

    PATH:
    %ANDROID_HOME%\platform-tools
