在 Linux 上设置 Android SDK 环境
========================================================

1. 安装 Android 命令行工具。
   前往 `Android Developer <https://developer.android.com/studio>`_ 并下载与你的操作系统匹配的工具。

   .. image::  ../../images/android-command-line-tool.png
       :align: center

   |

   | 你可以在命令行中使用 ``wget`` 下载工具下载压缩包，也可以从浏览器中下载并自行解压。

   你可以从上述 `Android Developer <https://developer.android.com/studio>`_ 网站复制下载链接。
   然后使用以下命令。

   .. code-block:: bash

       wget https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip?hl=zh-cn
       mkdir -p Android/cmdline-tools
       unzip commandlinetools-linux-11076708_latest.zip?hl=zh-cn -d Android/cmdline-tools
       mv Android/cmdline-tools/cmdline-tools Android/cmdline-tools/latest

2. 配置相关环境。

   安装 Java。（如果你之前已经安装并配置过Java，你需要检查你的 JDK 是否与命令行工具适配。如果版本适配，你可以跳过以下关于 Java 环境配置的步骤）

   | 我们使用 ``JDK-17`` 来运行安卓模拟器。。

   .. code-block:: bash

       sudo apt install openjdk-17-jdk

   打开你的 ``.bashrc`` 文件。

   .. code-block:: bash

       sudo nano ~/.bashrc

   在文件末尾添加以下内容。

   .. code-block:: bash

       export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
       export PATH=$PATH:$JAVA_HOME/bin
       export ANDROID_HOME=$HOME/Android
       export PATH="$ANDROID_HOME/emulator:$ANDROID_HOME/tools:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/tools/bin:$ANDROID_HOME/cmdline-tools/latest:$ANDROID_HOME/platform-tools:$PATH"

   | 确保 ``PATH`` 配置与你存储相关工具的路径匹配。

   最后，重新装载 ``.bashrc`` 文件，使更改立即应用于当前终端会话。

   .. code-block:: bash

       source ~/.bashrc

3. 验证 ``sdkmanager`` 是否成功安装。
   .. code-block:: bash

       sdkmanager --update
       sdkmanager --list
       sdkmanager --licenses

   如果你获得如下信息，则安装成功。

   .. image::  ../../images/sdkmanager-licenses.png
       :align: center

   |

   你可以从 `sdkmanager 的常用命令 <https://developer.android.com/tools/sdkmanager>`_ 了解更多。

WSL 常见问题
--------------------------------------

**1. WSL 依赖项**

请将你的 Windows 升级到 Win11，并使用 WSL 2。这将解决大多数 Win10 和 WSL 1 中的 WSL 问题。

**2. WSL PATH 设置**

默认情况下，WSL 将共享 Windows 系统中的环境变量。有时这会导致错误的行为。
你可能会发现你使用的实际可执行文件并不是你通过 ``which`` 命令找到的文件。此问题的根本原因是：WSL 中的 ``which`` 命令只能找到 WSL 的 PATH 中的可执行文件。但是，如果你在 Windows PATH 和 WSL PATH 中同时配置了一个可执行文件（例如 python3），而 Windows PATH 在 WSL PATH 之前设置（``PATH=$Windows_PATH:$WSL_PATH``）。那么你使用的实际可执行文件就是 Windows_PATH 中的文件。但你通过 ``which`` 找到的则是 WSL_PATH 中的文件。

要解决此问题，你可以按照以下建议操作：

- 在设置 PATH 时将你的环境 PATH 放在前面

    使用 ``PATH=New_PATH:$PATH`` 而不是 ``PATH=$PATH:New_PATH``。这是一个良好的习惯，可以优先考虑你的最新设置并确保其始终有效。

- 禁用环境变量的共享

    .. code-block:: bash

        # WSL bash
        sudo vim /etc/wsl.conf

        # 添加以下内容
        [interop]
        appendWindowsPath = false

        # 在 PowerShell 中重启 WSL 
        wsl --shutdown

**3. CPU 硬件加速问题**

.. error:: 
    
    This user doesn't have permissions to use KVM (/dev/kvm), ERROR: x86 emulation currently requires hardware acceleration!

.. image:: ../../images/issues1.png
    :align: center

|

请遵循 `Stack Overflow - Android Studio: /dev/kvm device permission denied <https://stackoverflow.com/questions/37300811/android-studio-dev-kvm-device-permission-denied>`_ 中的第一个解决方案。
然后，注销并重新登录Linux。

.. code-block:: bash

    sudo adduser $USER kvm
    sudo chown $USER -R /dev/kvm
