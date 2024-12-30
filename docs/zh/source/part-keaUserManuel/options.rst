Kea 的参数选项
=====================================

Kea 的参数
-------------------------------------

Kea 提供了以下选项。使用 ``kea -h`` 查看详细信息。

以下参数是 kea 中最重要的参数。大多数时候，你需要指定它们。

``-f``：包含性质的测试文件。你可以针对多个文件运行多个性质。参见 :ref:`target_multiple_properties`。

``-a --apk``：被测试应用的安装包文件或包名。

``-d --device_serial``：用于测试的设备的序列号。（当只连接了一个设备时，此参数可缺省，kea将自动指定目标设备。你可以使用 'adb devices' 或 'hdc list targets' 查找你的目标设备）

``-o --output``：执行结果的输出目录。（默认："output"）

``-p --policy``：探索策略的名称。（**"random"**、**"guided"** 或 **"llm"**）

``-is_emulator``：声明目标设备为模拟器。

以下是启动 kea 的一些示例。

.. code-block:: bash
    
    # 快速开始，默认随机策略，输出到 "output" 目录
    kea -f my_property.py -a myapp.apk

    # 自定义策略
    kea -f my_property.py -a myapp.apk -p guided

    # 使用多个性质
    kea -f my_property1.py my_property2.py -a myapp.apk
    
    # 自定义输出目录
    kea -f my_property.py -a myapp.apk -o my_output

    # 当有多台设备连接到你的电脑时，指定目标设备
    kea -f my_property.py -a myapp.apk -d emulator-5554 -is_emulator
    
以下是用于自定义 kea 的命令。

``-t --timeout``：测试时间（秒）。

``-n``：每 n 个事件后，重新启动应用，默认为100。

``-debug``：以调试模式运行（输出调试信息）。

``-keep_app``：测试后保留设备上的应用。

``-grant_perm``：安装时授予所有权限。对 Android 6.0+ 有用。

``-is_harmonyos``：使用 HarmonyOS 设备

``-load_config``：从 config.yml 加载配置。config.yml 中的设置将覆盖命令行参数。

``-utg``：生成UTG图。

.. _yml_config:

YAML 配置
--------------

你可以使用 YAML 配置来启动 kea。在你的 kea 根目录中找到 ``config.yml``。

config.yml 文件用于简化通过配置文件指定参数的过程。请注意，config.yml 中的参数值将覆盖通过命令行指定的参数值。

**配置参数对应关系**

以下是 config.yml 文件中的参数与 Kea 参数对象中的对应关系：

system: 对应 -is_harmonyos，用于指定是否使用 HarmonyOS 设备。

app_path, package, package_name: 这些参数对应 -a，用于指定应用的 apk 文件路径或包名。

policy: 对应 -p，用于指定探索策略。

output_dir: 对应 -o，用于指定执行结果的输出目录。

count: 对应 -n，用于指定测试次数。

target, device, device_serial: 这些参数对应 -d，用于指定测试使用的设备序列号。

property, properties, file, files: 这些参数对应 -f，用于指定包含性质的测试文件列表。

以下是配置的示例。

.. code-block:: yaml

    # env: 你的电脑系统（例如 windows, macOS, Linux）
    env: Linux

    # system: 目标系统
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

一旦完成配置，你可以简单地使用 ``kea -load_config`` 启动 kea。

.. important:: 
    当你在 HarmonyOS 上使用 kea 时，config.yml 是必需的。

.. _target_multiple_properties:

当运行多个性质时 kea 做了什么？
--------------------------------------------------------
默认情况下，随机和主路径引导探索策略在每次运行中验证应用的一个性质。
当应用有多个性质可用时，这两种策略可以一起验证这些性质的任何子集。
一个好处是 Kea 可以提高验证性质的效率。
另一个好处是多个性质的交互场景提供了应用的部分模型。
这个部分模型使我们更有可能在测试期间达到应用的更深层次状态。

具体来说，要一起验证多个性质，随机策略会检查
多个性质的前提条件是否满足，并随机选择一个性质进行检查。
主路径引导探索策略会随机选择一个性质作为目标，
并沿着其主路径进行引导探索。当这个主路径上的每个状态都被探索后，
这种策略会随机选择另一个性质作为新目标。
此外，当多个性质的前提条件满足时，这种策略会随机选择一个性质进行检查。

你可以在 :ref:`kea_mechanism` 中查看详细信息。
