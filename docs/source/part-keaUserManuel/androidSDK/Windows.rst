在 Windows 上设置 Android SDK 环境
========================================================

1. 安装 Android 命令行工具。
   前往 `Android Developer <https://developer.android.com/studio>`_ 并下载与你的操作系统匹配的工具。

   .. image::  ../../images/android-command-line-tool.png
       :align: center

   |

   将下载的 ZIP 文件解压到你希望安装 SDK 的目录中。

   将 ``cmdline-tools`` 文件夹中的内容移动到最新文件夹中。最终结构应为：

   .. code-block::

       D:\AndroidSDK\cmdline-tools\latest

2. 配置相关环境。

   安装 Java。（如果你之前已经安装并配置过Java，你需要检查你的 JDK 是否与命令行工具适配。如果版本适配，你可以跳过以下关于 Java 环境配置的步骤）

   访问 `Oracle JDK <https://www.oracle.com/java/technologies/downloads/#jdk21-windows>`_ 的官方网站，选择适合 Windows 的版本并下载。

   | 在这里，你可以使用 ``JDK-21``。

   然后运行下载的安装程序，按照提示完成安装。
   确保记下安装路径以备将来参考。

   .. code-block::

       D:\Java\jdk-21

3. 设置环境变量。

   打开环境变量设置：

   - 右键单击 ``此电脑`` 或 ``计算机``，选择 ``属性``。
   - 点击 ``高级系统设置``。
   - 在 ``系统属性`` 窗口中选择 ``环境变量``。

   |

   在 ``系统变量`` 部分，点击 ``新建`` 添加 ``JAVA_HOME`` 变量，值设置为 JDK 安装路径（``D:\Java\jdk-21``）。
   并添加 ``ANDROID_HOME`` 变量，值设置为 AndroidSDK 安装路径（``D:\AndroidSDK``）。

   找到 ``Path`` 变量，点击 ``编辑``，然后添加 ``%JAVA_HOME%\bin``、``%ANDROID_HOME%\tools``、``%ANDROID_HOME%\emulator``、``%ANDROID_HOME%\cmdline-tools\latest\bin``、
   ``%ANDROID_HOME%\tools\bin``、``%ANDROID_HOME%\cmdline-tools\latest`` 和 ``%ANDROID_HOME%\platform-tools``。

4. 验证安装

   打开命令提示符：按 ``Win + R``，输入 cmd，然后按 ``Enter``。

   在命令提示符窗口中，输入 ``java -version`` 和 ``javac -version``，然后按 Enter。

   .. code-block:: bash

       java -version
       javac -version
       sdkmanager --version

   如果显示版本信息，则表示配置成功。

5. 验证 ``sdkmanager`` 是否成功安装。

   .. code-block:: bash

       sdkmanager --update
       sdkmanager --list
       sdkmanager --licenses

   在这里，你应该会看到信息显示 ``All SDK package licenses accepted``。

   你可以从 `sdkmanager 的常用命令 <https://developer.android.com/tools/sdkmanager>`_ 了解更多。
