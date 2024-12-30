在 MAC OS 上设置 Android SDK 环境
========================================================

1. 安装 Android 命令行工具。
   前往 `Android Developer <https://developer.android.com/studio>`_ 并下载与你的操作系统匹配的工具。

   .. image::  ../../../../images/android-command-line-tool.png
       :align: center

   |

   | 你可以在命令行中使用 ``wget`` 下载工具下载压缩包，也可以从浏览器中下载并自行解压。

   你可以从上述 `Android Developer <https://developer.android.com/studio>`_ 网站复制下载链接。
   然后使用以下命令。

   .. code-block:: bash

       wget https://dl.google.com/android/repository/commandlinetools-mac-11076708_latest.zip?hl=zh-cn
       mkdir -p Android/cmdline-tools
       unzip commandlinetools-mac-11076708_latest.zip?hl=zh-cn -d Android/cmdline-tools
       mv Android/cmdline-tools/cmdline-tools Android/cmdline-tools/latest

2. 配置相关环境。

   安装 Java。（如果你之前已经安装并配置过Java，你需要检查你的 JDK 是否与命令行工具适配。如果版本适配，你可以跳过以下关于 Java 环境配置的步骤）

   | 我们使用 ``JDK-17`` 来运行安卓模拟器。。

   .. code-block:: bash

       sudo brew install openjdk@17

   打开你的 ``.bashrc`` 文件。

   .. code-block:: bash

       sudo nano ~/.zshrc

   在文件末尾添加以下内容。

   .. code-block:: bash

       export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"
       export ANDROID_HOME="/Users/your_id_name/the_path_you_store_commandline_tools/Android"
       export PATH="$ANDROID_HOME/emulator:$ANDROID_HOME/tools:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/tools/bin:$ANDROID_HOME/cmdline-tools/latest:$ANDROID_HOME/platform-tools:$PATH"

   | 确保 ``PATH`` 配置与你存储相关工具的路径匹配。

   最后，重新装载 ``.zshrc`` 文件，使更改立即应用于当前终端会话。

   .. code-block:: bash

       source ~/.zshrc

3. 验证 ``sdkmanager`` 是否成功安装。

   .. code-block:: bash

       sdkmanager --update
       sdkmanager --list
       sdkmanager --licenses

   如果你获得如下信息，则安装成功。

   .. image::  ../../../../images/sdkmanager-licenses.png
       :align: center

   |

   你可以从 `sdkmanager 的常用命令 <https://developer.android.com/tools/sdkmanager>`_ 了解更多。
