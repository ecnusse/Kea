InputManager
================

本部分旨在解释 Kea 的中的策略及输入控制器类 InputManager 的设计与实现。


功能设计与实现
------------------

InputManager类是事件生成器的控制类，负责启动、停止事件的生成，
并负责根据指定的输入策略生成和发送事件，支持随机探索策略、主路径引导策略和LLM策略。
该类提供了灵活的事件管理机制，允许用户自定义事件生成策略，并能够根据应用的运行状态动态调整事件发送。
InputManager所包含的主要方法有：

- 获取当前测试用户所选择的探索策略。
- 添加事件到设备的执行事件列表等待执行。
- 使用当前探索策略开始生成事件进行测试。
- 停止生成事件，结束此次测试。

.. figure:: ../../images/input_manager.png
    :align: center

    InputManager 类的组成

.. note::
        
    为了便于读者理解，本文中提供的代码段简化版本仅对核心流程进行抽象并展示，实际代码与简化的参考代码不完全一致。

类属性
--------

- ``DEFAULT_POLICY``: 默认的输入策略名称。
- ``RANDOM_POLICY``: 随机输入策略名称。
- ``DEFAULT_EVENT_INTERVAL``: 默认事件间隔时间。
- ``DEFAULT_EVENT_COUNT``: 默认生成事件的数量。
- ``DEFAULT_TIMEOUT``: 默认超时时间。
- ``DEFAULT_DEVICE_SERIAL``: 默认设备序列号。
- ``DEFAULT_UI_TARPIT_NUM``: 默认UI陷阱数量。

InputManager类中的数据结构
---------------------------

1. **device**

   device是Device的对象，用于记录当前测试的设备信息,便于后续对设备的交互操作。

2. **app**
   
   app是App的对象，用于记录当前所测试的移动应用的信息。

3. **policy & policy_name**
   
   policy_name是string类型，用于存储用户所选择的探索策略名。policy是具体探索策略类的对象。

4. **event_count & event_interval & number_of_events_that_restart_app**
   
   这三个成员变量均为整型。event_count记录从测试开始到现在生成的事件个数；event_interval记录了用户设置的两个事件之间停顿的时间；
   number_of_events_that_restart_app为多少个事件后需要重启应用程序。

5. **kea**
   
   kea为Kea类的对象，用于生成事件过程中从Kea类中取出记录数据来完成对应用性质的测试。

6. **enabled**
   
   enabled为bool类型，用于记录当前事件生成器是否需要继续生成事件，默认值为True。

7. **generate_utg**

   enerate_utg为bool类型用于记录用户所设置的是否生成UI转移图的参数，便于生成事件的过程中判断是否应该生成UI转移图。

8. **sim_caculator**

   sim_caculator为Similarity的对象，用于计算上一个界面状态与当前界面状态之间的相似性。

InputManager类中的成员方法
---------------------------

构造函数
~~~~~~~~~~~~~~~

``__init__`` 方法用于初始化InputManager实例，设置事件发送的基本参数，并根据提供的策略名称初始化对应的输入策略。

:参数:
   - ``device``: Device实例，表示目标设备。
   - ``app``: App实例，表示目标应用。
   - ``policy_name``: 字符串，指定生成事件的策略名称。
   - ``random_input``: 布尔值，指示是否使用随机输入。
   - ``event_interval``: 事件间隔时间。
   - ``event_count``: 事件生成数量，默认为``DEFAULT_EVENT_COUNT``。
   - ``profiling_method``: 分析方法，用于性能分析。
   - ``kea``: Kea实例，用于性质测试。
   - ``number_of_events_that_restart_app``: 重启应用的事件数量。
   - ``generate_utg``: 布尔值，指示是否生成UTG。

:核心流程:
   1. 初始化日志记录器。
   2. 设置事件发送参数。
   3. 根据策略名称初始化输入策略。
   4. 设置相似度计算器。

获取探索策略的方法
~~~~~~~~~~~~~~~~~~~~~~~

1. **get_input_policy**

    get_input_policy 方法根据用户所选择的policy_name来实例化对应的探索策略对象。
    实例化的对象存储在policy成员变量里。支持的策略包括：随机探索策略、主路径引导策略和LLM策略。

    :参数:
      - ``device``: Device实例。
      - ``app``: App实例。

    :返回:
      - 本次测试使用的策略实例。

    :核心流程:
      1. 根据策略名称判断使用哪种输入策略。
      2. 创建对应的输入策略实例。
   
    .. code-block:: python

        def get_input_policy(self, device, app):
            if self.policy_name == POLICY_NONE:
                input_policy = None
            elif self.policy_name == POLICY_GUIDED:
                input_policy = GuidedPolicy(device,app,self.kea,self.generate_utg)
            elif self.policy_name == POLICY_RANDOM:
                input_policy = RandomPolicy(device, app, self.kea, self.number_of_events_that_restart_app, True, self.generate_utg)
            elif self.policy_name == POLICY_LLM:
                input_policy = LLMPolicy(device, app, self.kea, self.number_of_events_that_restart_app, True, self.generate_utg)
            else:
                input_policy = None
            return input_policy

事件生成器的控制方法
~~~~~~~~~~~~~~~~~~~~~~~

1. **start**
   
   start 方法用于启动所选定的探索策略。

   :核心流程:
      1. 记录开始发送事件的日志。
      2. 根据输入策略开始发送事件。
      3. 处理键盘中断，确保优雅退出。

   .. code-block:: python

        def start(self):
            try:
                if self.policy is not None:
                    self.policy.start(self)
            except KeyboardInterrupt:
                pass
            self.stop()

2. **stop**
   
   stop 方法用于结束探索过程。

   :核心流程:
      1. 终止事件发送。
      2. 清理事件发送相关的资源。
      3. 记录停止发送事件的日志。

   .. code-block:: python

        def stop(self):
            self.enabled = False

3. **add_event**
   
   add_event添加一个事件到事件列表，并将该事件发送给移动设备。
   
   :参数:
      - ``event``: 要添加的事件，应为AppEvent的子类。

   :核心流程:
      1. 将事件添加到事件列表。
      2. 创建事件日志记录器。
      3. 根据事件间隔时间发送事件到设备。

   .. code-block:: python

        def add_event(self, event):
            if event is None:
                return
            self.events.append(event)
            event_log = EventLog(self.device, self.app, event)
            event_log.start()
            while True:
                time.sleep(self.event_interval)
                if not self.device.pause_sending_event:
                    break
            event_log.stop()

使用方法
--------

InputManager类的主要作用是控制事件生成器并管理应用运行期间的事件发送。
用户可以通过构造函数初始化InputManager实例，并设置相应的参数，如测试设备、被测应用、策略名称等。
然后，可以通过start方法启动事件生成器。通过add_event方法添加单个事件，并发送。通过stop方法停止生成事件。