Kea's args options
=====================================

Kea's args
-------------------------------------

Kea provides the following options. Use ``kea -h`` for details.

The following args are the most important args in kea. You'll need to specify them most of the time.

``-f``: The test files that contain the properties. You can target multiple files to run multiple properties. See :ref:`target_multiple_properties`.

``-a --apk``: The apk file of the app under test.

``-d --device_serial``: The serial number of the device used in the test. (use 'adb devices' to find your target device)

``-o --output``: The output directory of the execution results. (default: "output")

``-p --policy``: The policy name of the exploration. (**"random"** or **"guided"**)

``-is_emulator``: Declare the target device to be an emulator, which would be treated specially.

Here's some example to launch kea.

.. code-block:: bash
    
    # quick start, random policy (default), output to "output" dir
    kea -f my_property.py -a myapp.apk

    # customize policy
    kea -f my_property.py -a myapp.apk -p guided

    # use multiple properties
    kea -f my_property1.py my_property2.py -a myapp.apk
    
    # customize output dir
    kea -f my_property.py -a myapp.apk -o my_output

    # target a device when there are multiple devices connected to your PC
    kea -f my_property.py -a myapp.apk -d emulator-5554 -is_emulator
    
The following commands are for customizing kea. You may find them helpful.

``-t --timeout``: The maximum testing time(seconds).

``-n``: Every n events, then restart the app.

``-debug``: Run in debug mode (dump debug messages).

``-keep_app``: Keep the app on the device after testing.

``-grant_perm``: Grant all permissions while installing. Useful for Android 6.0+.


``-is_harmonyos``: use harmonyos devices

``-load_config``: load config from config.yml. The setting in config.yml will cover the commandline args.

.. _yml_confg:

YAML config
--------------

You can use YAML config to launch kea. Find out the ``config.yml`` in your kea root dir.

Here's an example of configuration.

.. code-block:: yaml

    # env: the system of your PC (e.g. windows, macOS, Linux)
    env: Linux

    # system: the target harmonyOS
    system: android
    # system: harmonyOS

    device: emulator-5554
    app_path: example/omninotes.apk
    policy: guided
    count: 100
    properties: 
    - example/example_property.py
    - example/example_mainpath_property.py
    #  - example/advanced_example_property.py

You can simply use ``kea -load_config`` to start kea once you done your configuration.

.. important:: 
    When you use kea for harmonyOS, config.yml is necessary.

.. _target_multiple_properties:

What does kea do when running multiple properties?
--------------------------------------------------------
The random and main path guided exploration strategies by default validate one property of an app at one run.
When multiple properties of an app are available,these two strategies can validate any subset of these properties together.
One benefit is that Kea can improve the efficiency of validating properties.
Another benefit is that the interaction scenarios of multiple properties provide a partial model of the app.
This partial model enables us more likely to reach deeper app states during testing.

Specifically, to validate multiple properties together, the random strategy would check
whether multiple properties’ preconditions are satisfied, and randomly select one property for checking.
The main path guided exploration strategy would randomly select one property as the target,
and perform guided exploration along its main path. When every state on this main path has been explored,
this strategy would randomly select another property as a new target.
In addition, this strategy would randomly select a property for check when multiple properties’ preconditions are satisfied.

You can checkout the animation in :ref:`kea_mechanism` for details.