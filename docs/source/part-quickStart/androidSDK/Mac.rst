Set up Android SDK Environment on MAC OS
========================================================

1. Install the Android Command Line Tools.
    Go to `Android Developer <https://developer.android.com/studio>`_ and Download the tools that match your operating system.

    .. image::  ../../../images/android-command-line-tool.png
        :align: center

    |

    | Here you can use ``wget`` to download the tool, you can download it directly if you want.

    You can copy the download link copy from the `Android Developer <https://developer.android.com/studio>`_ website mentioned above.
    And then use following commands.

    .. code-block:: bash

        wget https://dl.google.com/android/repository/commandlinetools-mac-11076708_latest.zip?hl=zh-cn
        mkdir -p Android/cmdline-tools
        unzip commandlinetools-mac-11076708_latest.zip?hl=zh-cn -d Android/cmdline-tools
        mv Android/cmdline-tools/cmdline-tools Android/cmdline-tools/latest

2. Configure the related environment.

    Install Java. (If you have already installed and configured it before, you should
    check if your JDK match the Command Line Tools and then skip the following steps about Java)

    | Here you can use ``JDK-17`` to match the latest tool available now.

    .. code-block:: bash

        sudo brew install openjdk@17

    Open your ``.bashrc`` file.

    .. code-block:: bash

        sudo nano ~/.zshrc

    add the following contents at the end of the file.

    .. code-block:: bash

        export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"
        export ANDROID_HOME="/Users/your_id_name/the_path_you_store_commandline_tools/Android"
        export PATH="$ANDROID_HOME/emulator:$ANDROID_HOME/tools:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/tools/bin:$ANDROID_HOME/cmdline-tools/latest:$ANDROID_HOME/platform-tools:$PATH"

    | Ensure that the ``PATH`` configuration matches the path where you have stored the relevant tools.

    Finally,  reloads the ``.zshrc`` file, applying changes to the current terminal session immediately.

    .. code-block:: bash

        source ~/.zshrc

3. Verify if ``sdkmanager`` is installed successfully.
    .. code-block:: bash

        sdkmanager --update
        sdkmanager --list
        sdkmanager --licenses

    If you get information similar to the following, the installation is successful.

    .. image::  ../../../images/sdkmanager-licenses.png
        :align: center

    |

    Common commands for sdkmanager. You can learn from `this link <https://developer.android.com/tools/sdkmanager>`_.

