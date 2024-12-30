HMDroidbot
====================

HMDroidbot是kea在应用探索阶段与安卓设备交互的类。主要提供生成事件，截图等方法。HMDroidbot同时提供一个UTG(UI Transition Graph, 事件迁移图)。
可以基于事件迁移图，以基于模型的测试(MBT, Model Based Testing)编写更高级的应用探索策略。

.. note:: 

    HMDroidbot为本项目工作的一部份，为队伍中梁锡贤同学开发，开发过程参考项目为droidbot，应计入本项目工作。

    https://github.com/ecnusse/HMDroidbot

HMDroidbot项目架构
~~~~~~~~~~~~~~~~~~~~~~~~~~

HMDroidbot项目架构组成部分有：

1. AppHM： 用于解析鸿蒙应用安装包(.hap)或鸿蒙包(package)。提供EntryAbility等信息。
2. DeviceHM： 一个鸿蒙设备的抽象，提供设备层面的一些操作接口，如发送文件，输入内容，旋转设备，获取前台应用等。
3. HDC： 鸿蒙设备hdc指令的抽象，提供通过hdc与设备交互的接口，如shell，pull_file等。DeviceHM依赖于本类。
4. Dumper： 鸿蒙设备获取界面布局的抽象类，HDC依赖于该类
5. hmdriver2： 鸿蒙设备测试工具hmdriver2，为DeviceHM拓展提供输入事件等功能。
6. InputManager： 输入控制器，提供策略选择等功能。
7. InputPolicy： 输入策略，提供多种输入策略，如随机策略，大模型指引策略等，用于规定探索应用的规则。
8. EventLog： 事件日志的抽象，执行事件输入前，事件输入后的记录操作，以及发送事件的操作。
9. InputEvent： 输入事件的类，包含点击、长按、输入等事件。
10. UTG： 事件迁移图(UI Transition Graph)的类，用于应用建模，可以被输入策略使用进行更复杂的决策。
11. DeviceState： 用于应用界面抽象的类，对应用界面进行不同层次的抽象，提供给UTG类进行建模。

.. figure:: ../../../../images/hmdroidbot.png
    :align: center

    HMDroidbot 项目架构图

因为InputManager, InputPolicy与Kea的输入策略重点相关，故另开章节进行介绍。hmdriver2为参考的框架，未做开发修改。
以下介绍除上述三个功能外的其他组成部分。其中EventLog、InputEvent、UTG基本复用droidbot。

AppHM
~~~~~~~~~~~~~~~~~~~

AppHM是一个鸿蒙应用的抽象，用于分析一个鸿蒙应用。对外提供对鸿蒙应用的分析方法，获取应用入口(EntryAbility)等信息。

AppHM会根据传入的应用是一个安装包(.hap)或一个包名(如com.example.app)，选择对应的方法进行初始化。

.. code-block:: 

    def __init__(self):

        if app_name is a installation package file:
            self._hap_init()
        elif app_name is a package name:
            self._package_init()

以下是AppHM的方法和文档：

.. csv-table:: 
    :header: "方法", "输入", "输出", "简介"

    "hap_init", "app_path:str", "", 给定一个安装包路径，通过安装包初始化app
    "load_hap_info", "pack_info:Dict", "", 对安装包进行解压缩，读取其中信息
    "package_init", "package_name:str", "", 通过包名初始化app
    "dumpsys_package_info", "", "package_info:Dict", 从dumpsys指令获取包信息 
    "get_package_name", "", "package_name:str", 获取app包名
    "get_start_intent", "", "start_intent:Intent", 获取启动应用的Intent
    "get_stop_intent", "", "start_intent:Intent", 获取停止应用的Intent
    "get_hashes", "", "hashes:List[str]", 获取应用安装包的哈希

DeviceHM
~~~~~~~~~~~~~~~~~

DeviceHM是一个鸿蒙设备的抽象，提供设备层面的一些操作接口，如发送文件，输入内容，旋转设备，获取前台应用等。

以下是DeviceHM的方法和文档。

.. note:: 

    设备适配器(adapters)是终端与应用进行交互的适配器，DeviceHM可以通过多种不同的工具与终端交互。
    如HDC、hmdriver2等。

.. csv-table:: 
    :header: "方法", "输入", "输出", "简介"

    "check_connectivity", "", "", 检查设备和设备适配器是否可用
    "set_up", "", "", 初始化设备和设备适配器
    "connect", "", "", 连接设备和设备适配器
    "disconnect", "", "", 断开设备和设备适配器
    "is_foreground", "app:AppHM", "Boolean", 检查某个应用是否在设备中处于前台状态
    "model_number", "", "model_number:str", 获取设备的设备号
    "device_name", "", "device_name:str", 获取设备名称
    "get_release_version", "", "sdk_api:str", 获取设备的SDK API版本
    "get_display_info", "", "display_info:Dict", 获取设备的分辨率
    "get_width", "", "width:str", 获取设备横向分辨率
    "get_height", "", "height:str", 获取设备纵向分辨率
    "unlock", "", "", 解锁设备
    "send_intent", "intent:Intent", "", 向设备中发送一个Intent
    "send_evnet", "event:InputEvent", "", 向设备发送一个事件
    "start_app", "app:AppHM", "", 启动一个应用
    "get_top_activity_name", "", "top_ability_name", 获取设备的栈顶Ability名称
    "get_current_activity_stack", "", "current_ability_stack:List[str]", 获取设备的Ability栈
    "install_app", "app:AppHM", "", 安装一个应用
    "uninstall_app", "app:AppHM", "", 卸载一个应用
    "push_file", "local_file:Path, remote_dir:Path", "", 推送一个文件到设备上
    "pull_file", "remote_file:Path, local_file:Path", "", 从设备拉取一个文件
    "take_screenshot", "", "", 对设备进行截图
    "get_current_state", "action_count:int", "current_state:DeviceState", 获取当前设备的状态抽象
    "view_touch", "x:int, y:int", "", 根据坐标执行点击操作
    "view_long_touch", "x:int, y:int, duration:float", "", 根据坐标执行长按操作
    "view_drag", "start_xy:List[int], end_xy:List[int], duration:float", "", 根据坐标执行拖动操作
    "view_append_text", "text:str", "", 添加一个文本
    "view_set_text", "text:str", "", 设置一个文本
    "key_press", "key_code", "", 根据事件代码输入一个事件
    "get_views", "get_views", "", 获取当前设备上的控件
    "get_random_port", "", "port:int", 随机获取一个可用端口

HDC
~~~~~~~~~~

鸿蒙设备hdc指令的抽象，提供通过hdc与设备交互的接口，如shell，pull_file等。DeviceHM依赖于本类。

鸿蒙设备通过Dumper类获取应用的界面。Dumper类是一个抽象类，共有两种实现：UitestDumper和HiDumper。

.. figure:: ../../../../images/hdc_dumpers.png
    :align: center

    Dumper 类与 HDC 类的关系示意


以下是HDC的方法和文档。

.. csv-table:: 
    :header: "方法", "输入", "输出", "简介"

    "set_up", "", "", 初始化HDC
    "run_cmd", "", "", 执行一个 hdc 命令行命令
    "shell", "", "", 执行一个 hdc shell 命令行命令
    "connect", "", "", 连接HDC 
    "disconnect", "", "", 断开HDC 
    "check_connectivity", "", "", 检查HDC是否可用
    "get_property", "property_name", "preoperty", 通过hdc获取设备的属性
    "get_model_number", "", "model_number:str", 获取设备的模型号
    "get_sdk_version", "", "sdk_version:str", 获取SDK版本
    "get_device_name", "", "", 获取设备名称
    "get_installed_apps", "", "installed_apps:List[str]", 获取已安装的应用
    "get_display_density", "", "dpi:str", 获取设备显示的dpi
    "unlock", "", "", 通过hdc解锁设备
    "touch", "x:int, y:int", "", 通过hdc根据坐标执行点击操作
    "long_touch", "x:int, y:int, duration:float", "", 通过hdc根据坐标执行长按操作
    "drag", "start_xy:List[int], end_xy:List[int], duration:float", "", 通过hdc根据坐标执行拖动操作
    "type", "text:str", "", 通过hdc添加一个文本
    "press", "key_code", "", 通过hdc根据事件代码输入一个事件
    "push_file", "local_file:Path, remote_dir:Path", "", 通过hdc推送一个文件到设备上
    "pull_file", "remote_file:Path, local_file:Path", "", 通过hdc从设备拉取一个文件
    "get_views", "output_dir", "", 获取当前页面的控件


Dumper主要从设备中获取当前页面的布局，并转换为安卓风格使droidbot能使用。

以下是UiTestDumper的实现：

.. csv-table:: 
    :header: "方法", "输入", "输出", "简介"

    "dump_view", "", "view_path", 通过uitest获取layout json，并返回
    "preprocess_views", "views_path", "", 处理views，转换为可双向查询的树结构
    "get_adb_view", "raw_view:Dict", "", 处理views，转换为安卓风格方便droidbot使用
    "get_view", "", "views:Dict", 获取views

以下是HiDumper的实现：

.. csv-table:: 
    :header: "方法", "输入", "输出", "简介"

    "get_focus_window", "", "focus_window", 获取当前前台窗口
    "dump_target_window_to_file", "focus_window:int, fp:IO", "", 拉取目标窗口的布局入文件中
    "dump_layout", "fp:IO", "", 根据hidumper的输出处理布局为树结构
    "adapt_hierachy", "", "", 处理布局为安卓风格
    “get_views", "", "views:Dict", 获取views


InputEvent
~~~~~~~~~~~~~~~~~

InputEvent是一个抽象类，其他所有的事件实现在此抽象接口上。

.. figure:: ../../../../images/input_event.png
    :align: center

    InputEvent接口和其实现

以下是InputEvent抽象类的方法：

.. csv-table:: 
    :header: "方法", "输入", "输出", "简介"

    "send", "device:HMDevice", "", 向设备发送事件
    "to_dict", "", "event_dict:Dict", 以字典形式保存当前事件
    "from_dict", "event_dict:Dict", "event:InputEvent", 从字典解析获取一个InputEvent实例
    "get_event_str", "state:DeviceState", "event_str:str", 根据当前状态获取事件表示
    "get_views", "", "views:List[str]", 获取当前事件对应的views

UTG
~~~~~~~~~~~~~~~~~~~~

事件迁移图(UI Transition Graph)的类，用于应用建模，可以被输入策略使用进行更复杂的决策。

以下是UTG的方法和文档。

.. csv-table:: 
    :header: "方法", "输入", "输出", "简介"

    "first_state_str", "", "state_str:str", 第一个事件的状态哈希
    "last_state_str", "", "state_str:str", 最后一个事件的状态哈希
    "effective_event_count", "", "count:int", 造成迁移的事件数量
    "nums_transitions", "", "count:int", 发现的状态迁移数量
    "clear_graph", "", "", 清除UTG
    "add_transition", "event:InputEvent, old_state:str, new_state:str", "", 添加一个迁移
    "remove_transition", "event:InputEvent, old_state:str, new_state:str", "", 删除一个迁移
    "add_node", "state:DeviceState, event:InputEvent", "", 添加一个状态节点
    "is_event_explored", "event:InputEvent, state:str", "Boolean", 判断一个事件是否已经执行过
    "is_state_reached", "state:str", "Boolean", 判断一个状态是否已经到达过
    "get_reachable_states", "current_state:str", "reachable_states:List[str]", 获取当前状态可迁移至的状态
    "reachable_from_one_state_to_another", "from_state:str, to_state:str", "Boolean", 判断两个状态是否可迁移
    "get_navigation_steps", "from_state:str, to_state:str", "List[Tuple[str, InputEvent]]", 获取从一个节点导航至另一个节点的步骤
    "find_activity_according_to_state_str", "state_str:str", "", 根据状态哈希获取状态对应的Ability

DeviceState
~~~~~~~~~~~~~~~~~~~~~

DeviceState是用于应用界面抽象的类，对应用界面进行不同层次的抽象，提供给UTG类进行建模。

以下是DeviceState的方法和文档。

.. csv-table:: 
    :header: "方法", "输入", "输出", "简介"

    "get_possible_input", "", "possible_input:List[InputEvent]", 获取当前状态上可执行的事件
    "get_text_representation", "", "state_desc:str, activity:str, indexed_views:List[str]", 获取当前状态的描述信息
    "get_view_by_attribute", "attribute_dict:Dict, random_select:Bool", 根据属性获取可用的控件
    "is_view_exist", "view_dict:Dict", "Boolean", 判断某个控件是否存在
    "get_view_desc", "view:Dict", "view_desc:str", 获取控件的描述
    "assemble_view_tree", "root_view:Dict, views:List[Dict]", "", 将view组织为树结构
    "get_view_str", "view:Dict", "view_str:str", 获取一个view的描述
    "get_pagePath", "", "pagePath:str", 获取当前界面对应的pagePath
    "get_state_str_raw", "", "state_str_raw:str", 获取当前页面的状态描述
    "get_state_str", "", "state_str:str", 获取当前页面的状态哈希
    "get_content_free_state_str", "", "content_free_str:str", 获取当前页面的结构哈希
    "save_view_img", "view_dict:Dict, output_dir:str", "", 保存控件截图

