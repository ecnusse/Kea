Set up Android SDK Environment on Linux
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

        wget https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip?hl=zh-cn
        mkdir -p Android/cmdline-tools
        unzip commandlinetools-linux-11076708_latest.zip?hl=zh-cn -d Android/cmdline-tools
        mv Android/cmdline-tools/cmdline-tools Android/cmdline-tools/latest

2. Configure the related environment.

    Install Java. (If you have already installed and configured it before, you should
    check if your JDK match the Command Line Tools and then skip the following steps about Java)

    | Here you can use ``JDK-17`` to match the latest tool available now.

    .. code-block:: bash

        sudo apt install openjdk-17-jdk

    Open your ``.bashrc`` file.

    .. code-block:: bash

        sudo nano ~/.bashrc

    add the following contents at the end of the file.

    .. code-block:: bash

        export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
        export PATH=$PATH:$JAVA_HOME/bin
        export ANDROID_HOME=$HOME/Android
        export PATH="$ANDROID_HOME/emulator:$ANDROID_HOME/tools:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/tools/bin:$ANDROID_HOME/cmdline-tools/latest:$ANDROID_HOME/platform-tools:$PATH"

    | Ensure that the ``PATH`` configuration matches the path where you have stored the relevant tools.

    Finally,  reloads the ``.bashrc`` file, applying changes to the current terminal session immediately.

    .. code-block:: bash

        source ~/.bashrc

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


Common issues for WSL
--------------------------------------

**1. WSL dependencies**

Please upgrade your windows to win11 and use WSL 2. This will can solve most of the WSL problem in win10 and WSL 1.

**2. WSL PATH settings**

By default, WSL will share the environmental variables in windows system. Sometimes this will lead to a wrong behavior.
You may find out that the real executable you use is not the one you found out with ``which`` cmd. The root cause of this issue
is: ``which`` command in WSL can only find out the executable in WSL's PATH. But if your have an executable (e.g. python3) configured
in windows PATH and WSL PATH simultaneously. While the windows PATH set before WSL PATH (``PATH=$Windows_PATH:$WSL_PATH``). The real 
executable you use is the one in Windows_PATH. But the one you found out with ``which`` is the one in WSL_PATH.

To solve this problem, you can follow these suggestion:

- Put your environment PATH first when setting PATH

    Use ``PATH=New_PATH:$PATH`` instead of ``PATH=$PATH:New_PATH``. This is a good habit to prioritize your settings
    and make sure it always work.

- Disable the the share of environmental variables

    .. code-block:: bash

        # WSL bash
        sudo vim /etc/wsl.conf

        # add the following content
        [interop]
        appendWindowsPath = false

        # reboot WSL in powershell 
        wsl --shutdown

**3. CPU acceleration issue**

This user doesn't have permissions to use KVM (/dev/kvm), ERROR: x86 emulation currently requires hardware acceleration!

        .. image:: ../../../images/issues1.png
            :align: center

        |

        Follow the first solution in the `link <https://stackoverflow.com/questions/37300811/android-studio-dev-kvm-device-permission-denied>`_.
        Then, Just log in again.

        .. code-block:: bash

            sudo adduser $USER kvm
            sudo chown $USER -R /dev/kvm