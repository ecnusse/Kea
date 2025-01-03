为 HarmonyOS 编写性质
=================================

HarmonyOS 的 UI 控件查看工具：uiviewer教程
-------------------------------------------------------

我们使用 uiviewer 来支持 HarmonyOS。以下命令将为你安装并启动 uiviewer。

.. code-block:: bash

    pip install -U uiviewer

    python -m uiviewer

这将启动一个主机服务器，默认情况下地址为 http://localhost:8000/。你可以通过浏览器访问该工具。


HarmonyOS PDL API 
---------------------------------------------------
我们使用 hmdriver2 作为 PDL API，与 uiautomator2 相似。

在 HarmonyOS 中，应用开发者指定的全局唯一的选择器是 **id** (类似安卓中的resourceId)。当没有id时，你可以使用 **text** 和 **description** 等属性来定位设备。
你可以在选择器中填写多个控件属性来确保尽可能准确地定位至目标控件。

你可以在 `github-hmdriver2 <https://github.com/codematrixer/hmdriver2>`_ 中查看 hmdriver2 的使用手册。

以下是一些 HarmonyOS PDL 的示例。

.. code-block:: python

    # 点击 id 为 "wifi_entry.icon" 的控件
    d(id="wifi_entry.icon").click()

    # 点击 id 为 "display_settings.title" 且text为 "Display" 的控件
    d(id="display_settings.title", text="Display").long_click()

    # 向 id 为 "url_input_in_search" 的控件输入 "hello"
    d(id="url_input_in_search").input_text("hello")

为 HarmonyOS 启动 Kea
----------------------------------------------

你应该在 ``config.yml`` 中指定你电脑的系统。你可以查看 :ref:`yml_config` 的教程。

以下是一个示例。

.. code-block:: yaml

    # config.yml

    # 声明电脑的系统为 Linux
    env: Linux 

你可以在终端或 config.yml 中指定其他参数。有关详细信息，请查看提供的
``config.yml``。

如果你在 config.yml 中指定了所有必要的参数，可以通过 ``kea -load_config`` 启动 kea。
以下示例是一个完全配置的示例，可以通过 ``kea -load_config`` 启动。

.. code-block:: yaml

    # env: 你电脑的系统 (例如 windows, macOS, Linux)
    env: Linux

    # system: 目标 HarmonyOS
    system: harmonyOS

    device: 127.0.0.1:5555          # 仅连接一个设备时可不填，就自动指定
    app_path: example/example.hap   # 应用安装包
    policy: random                  # 输入策略
    count: 100
    properties: 
        - example/example_hm_property.py
    
    # package 用于通过包名指定待测应用。此选项和通过app_path指定安装包请二选一。
    # 当你使用包名指定待测应用时，你一般需要让keep_app为True，这让测试停止时应用不会被卸载。
    package: com.youku.next
    keep_app: True

