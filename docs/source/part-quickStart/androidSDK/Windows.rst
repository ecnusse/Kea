Set up Android SDK Environment on Windows
========================================================

1. Install the Android Command Line Tools.
    Go to `Android Developer <https://developer.android.com/studio>`_ and Download the tools that match your operating system.

    .. image::  ../../../images/android-command-line-tool.png
        :align: center

    |

    Unzip the downloaded ZIP file to the directory where you want to install the SDK.

    Move the contents of the ``cmdline-tools`` folder into the latest folder. The final structure should be:

    .. code-block::

        D:\AndroidSDK\cmdline-tools\latest

2. Configure the related environment.

    Install Java. (If you have already installed and configured it before, you should
    check if your JDK match the Command Line Tools and then skip the following steps about Java)

    Visit the official website of `Oracle JDK <https://www.oracle.com/java/technologies/downloads/#jdk21-windows>`_, choice the version suitable for Windows and download it.

    | Here you can use ``JDK-21``

    Then run the downloaded installer and follow the prompts to complete the installation.
    Make sure to note the installation path for future reference.

    .. code-block::

        D:\Java\jdk-21

3. Set the environment variables.

    Open the environment variable settings:

    - Right-click on ``This PC`` or ``Computer`` and select ``Properties``.
    - Click on ``Advanced system settings``.
    - In the ``System Properties`` window, select ``Environment Variables``.

    |

    In the ``System Variables`` section, click ``New`` to add the ``JAVA_HOME`` variable, with the value set to the JDK installation path(``D:\Java\jdk-21``).
    And add the ``ANDROID_HOME`` variable, with the AndroidSDK installation path(``D:\AndroidSDK``).

    Locate the ``Path`` variable, click ``Edit``, then add ``%JAVA_HOME%\bin``, ``%ANDROID_HOME%\tools``, ``%ANDROID_HOME%\emulator``, ``%ANDROID_HOME%\cmdline-tools\latest\bin``,
    ``%ANDROID_HOME%\tools\bin``, ``%ANDROID_HOME%\cmdline-tools\latest`` and ``%ANDROID_HOME%\platform-tools``.

4. Verify Installation

    Open the Command Prompt: Press ``Win + R``, type cmd, and then press ``Enter``.

    In the Command Prompt window, type ``java -version`` and ``javac -version``, then press Enter.

    .. code-block:: bash

        java -version
        javac -version
        sdkmanager --version

    If version information is displayed, it indicates that the configuration was successful.

5. Verify if ``sdkmanager`` is installed successfully.
    .. code-block:: bash

        sdkmanager --update
        sdkmanager --list
        sdkmanager --licenses

    Here you should get information says ``All SDK package licenses accepted``.

    Common commands for sdkmanager. You can learn from `this link <https://developer.android.com/tools/sdkmanager>`_.

