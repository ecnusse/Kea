.. _llm:

LLMPolicy
================

LLMPolicy类是使用LLM（Large Language Model）在检测到UI陷阱时生成输入事件的核心类。
主要负责在应用状态空间中遇到难以探索的UI状态时，利用LLM生成输入事件以增强功能场景覆盖。
该类提供了完整的LLM辅助事件生成策略的事件生成过程。
LLMPolicy所包含的主要方法有：

- 根据当前状态生成一个LLM辅助的随机事件。
- 根据配置重启或重新安装应用。
- 在满足预条件的情况下，根据随机性决定是否检查性质。

LLM辅助事件生成策略的介绍
--------------------------

LLM辅助事件生成策略是一种结合了大型语言模型的策略，它可以在应用的GUI测试中遇到难以通过传统随机策略探索的状态时，利用LLM生成更有效的输入事件。
这种策略特别适用于那些需要深入探索应用状态空间或需要优化测试覆盖率的场景。

.. figure:: ../../../../images/llm_flowchart.png
    :align: center

    LLM辅助事件生成策略的流程图

具体执行步骤如下：

步骤1：开始执行 LLMPolicy 类的事件生成过程。

步骤2：初始化 LLMPolicy 实例，设置日志记录器、动作历史记录等。

步骤3：启动事件生成循环，直到输入管理器的事件计数结束或条件不再满足。

步骤4：检查事件计数器是否小于输入管理器设定的事件计数。

步骤5：如果事件计数器小于输入管理器设定的事件计数，获取当前应用状态。

步骤6：判断当前状态是否为空。

步骤7：如果当前状态为空，等待5秒并返回一个名称为"BACK"的键事件。

步骤8：如果当前状态不为空，检查是否检测到UI陷阱。

步骤9：如果检测到UI陷阱，检查模拟计数器是否超过了最大查询LLM次数。

步骤10：如果模拟计数器超过了最大查询LLM次数，记录日志并返回一个名称为"BACK"的键事件。

步骤11：如果模拟计数器未超过最大查询LLM次数，生成一个LLM事件。

步骤12：如果未检测到UI陷阱，生成一个随机事件。

步骤13：基于当前用户触发的事件（UTG）生成LLM事件。

步骤14：返回生成的事件，该事件将被用于与应用的交互。

步骤15：保存截图并将生成的事件添加到输入管理器。

步骤16：更新当前状态和最后事件。

步骤17：检查是否允许生成UTG。

步骤18：如果允许生成UTG，更新UTG。

步骤19：生成报告，包括所有状态和触发的bug信息。

步骤20：事件计数器加1，回到步骤4继续循环。

步骤21：如果事件计数器达到输入管理器设定的事件计数，结束事件生成循环。

步骤22：清理资源，结束 LLMPolicy 类的事件生成过程。

LLM辅助事件生成策略的伪代码
-----------------------------

:math:`\textbf{Algorithm:} LLM-Assisted Event Generation`

:math:`\textbf{Input:} None`
    
:math:`\textbf{Output:} Bug Report`

.. code-block::
    :linenos:

    Function LLM_Assisted_Event_Generation(policy_params)
        Initialize policy with device, app, kea, and other parameters
        Set event_count to 0

        While input_manager is enabled and event_count < max_events
            If device needs initialization
                Perform device initialization

            Determine current application state
            If app is not running
                Start the app
            ElseIf app is in background
                Bring app to foreground
            Else
                Generate LLM prompt based on current state and history
                Query LLM for next action
                If LLM response indicates action
                    Perform action and update state
                Else if LLM indicates text input
                    Get text from LLM and perform text input action
                End If
            End If

            If event_count is a multiple of restart_threshold
                Restart the app if necessary

            Save screenshot and add event to input_manager
            Increment event_count
        End While

        Generate final bug report if any issues found
        Clean up policy resources
    End Function
..
    Class LLMPolicy(RandomPolicy)
        Function __init__(device, app, kea, restart_app_after_check_property, number_of_events_that_restart_app, clear_and_restart_app_data_after_100_events, allow_to_generate_utg)
            Initialize logger, action histories, and other attributes
            Call super().__init__(device, app, kea)

        Function start(input_manager: InputManager)
            Initialize event_count
            While input_manager.enabled and event_count < input_manager.event_count
                If device.is_harmonyos is False and device has u2
                    Set fastinput_ime to True
                Log exploration action count
                Determine from_state based on to_state and device current state
                If event_count is 0
                    Create KillAppEvent
                ElseIf event_count is 1
                    Create IntentEvent with app start intent
                Else
                    If input_manager.sim_calculator detects UI tarpit and sim_count is below threshold
                        If sim_count exceeds MAX_NUM_QUERY_LLM
                            Log and go back, clear action history, reset sim_count
                        Else
                            Generate LLM event
                    Else
                        Generate random event
                If event is not None
                    Save screenshot and add event to input_manager
                    Update to_state and last_event
                    If allow_to_generate_utg, update UTG
                    Generate bug report
                Handle exceptions and increase event_count
            Tear down resources

        Function generate_llm_event()
            If event_count indicates app restart or last event is ReInstallAppEvent
                Run initializer and update from_state
            If current_state is None
                Sleep and return KeyEvent("BACK")
            If event_count is a multiple of number_of_events_that_restart_app and clear_and_reinstall_app is True
                Log and return ReInstallAppEvent
            Retrieve rules with satisfied preconditions
            If there are rules
                Log time needed to satisfy precondition
                If random choice is less than 0.5
                    Check property and possibly restart app
                Else
                    Log and do not check property
            If no event is generated
                Generate event based on UTG
            Handle device rotation events
            Return event

        Function generate_llm_event_based_on_utg()
            If app is not in activity stack
                Manage app restarts and return IntentEvent to start app
            ElseIf app is in activity stack but not in foreground
                Manage going back to app
            Else
                Generate action based on LLM query and current state
                If action is random
                    Select random action
                Else
                    Manage text input for SetTextEvent
                Return action

        Function _query_llm(prompt, model_name="gpt-3.5-turbo")
            Set up OpenAI client and send prompt to LLM
            Receive and return response

        Function _get_action_with_LLM(current_state, action_history, activity_history)
            Construct prompt with task, current state, and history
            Query LLM and receive response
            Parse response to get action index
            Select action and update histories
            If action is SetTextEvent
                Query LLM for text input
                Update action text
            Return action and candidate actions

        Function get_last_state()
            Return from_state

        Function clear_action_history()
            Reset action history


LLMPolicy类中的数据结构
---------------------------

1. **event_count**
   
   - ``event_count`` 整型，记录了已经生成的事件数量。

2. **number_of_events_that_restart_app**
   
   - ``number_of_events_that_restart_app`` 整型，记录了在重启应用前需要生成的事件数量。

3. **clear_and_restart_app_data_after_100_events**
   
   - ``clear_and_restart_app_data_after_100_events`` 布尔型，指示是否在100次事件后清除并重启应用数据。

4. **restart_app_after_check_property**
   
   - ``restart_app_after_check_property`` 布尔型，指示在检查性质后是否重启应用。

5. **_action_history**
   
   - ``_action_history`` 列表，记录了动作历史。

6. **_all_action_history**
   
   - ``_all_action_history`` 集合，记录了所有动作历史记录。

7. **_activity_history**
   
   - ``_activity_history`` 集合，记录了活动历史记录。

8. **from_state**
   
   - ``from_state`` 对象，记录了起始状态。

9. **task**
   
   - ``task`` 字符串，记录了LLM的任务描述。


LLMPolicy类中的成员方法
---------------------------

启动事件生成的方法
~~~~~~~~~~~~~~~~~~~~~~

**start**
   
``start`` 方法用于启动事件生成过程。

:参数:
   - input_manager: InputManager的实例。

:核心流程:
   1. 初始化事件计数器和输入管理器。
   2. 循环生成事件直到达到输入管理器设定的事件计数或条件不再满足。
   3. 根据当前状态和LLM的指导生成事件。
   4. 将生成的事件添加到输入管理器中并更新设备状态。
   5. 处理异常情况并在每次事件后增加事件计数器。

   .. code-block:: python
       :linenos:

        def start(self, input_manager):
            self.event_count = 0
            self.input_manager = input_manager
            while self.event_count < input_manager.event_count:
                event = self.generate_event()
                self.input_manager.add_event(event)
                self.event_count += 1

        def generate_event(self):
            if not self.from_state:
                self.from_state = self.device.get_current_state()
            if self.event_count == 0:
                event = KillAppEvent(app=self.app)
            elif self.event_count == 1:
                event = IntentEvent(self.app.get_start_intent())
            else:
                event = (self.generate_llm_event() 
                        if input_manager.sim_calculator.detected_ui_tarpit(input_manager)
                        else self.generate_random_event_based_on_current_state())
            return event

生成LLM事件的方法
~~~~~~~~~~~~~~~~~~~~~~

**generate_llm_event**
   
``generate_llm_event`` 方法用于生成一个LLM辅助的事件。

:参数:
   - 无

:返回:
   - 生成的事件对象。

:核心流程:
   1. 检查是否需要运行初始化器并获取当前应用状态。
   2. 根据事件计数和设置决定是否重启应用或清除并重新安装应用。
   3. 检查是否有满足前提条件的规则，并根据随机性决定是否检查性质。
   4. 生成基于LLM的事件。

   .. code-block:: python
       :linenos:

        def generate_llm_event(self):
            if self.event_count == START_TO_GENERATE_EVENT_IN_POLICY or isinstance(self.last_event, ReInstallAppEvent):
                self.run_initializer()
                self.from_state = self.device.get_current_state()
            if not self.from_state:
                time.sleep(5)
                return KeyEvent(name="BACK")

            if self.event_count % self.number_of_events_that_restart_app == 0 and self.clear_and_reinstall_app:
                return ReInstallAppEvent(self.app)

            rules_to_check = self.kea.get_rules_whose_preconditions_are_satisfied()
            if rules_to_check and random.random() < 0.5:
                self.check_rule_whose_precondition_are_satisfied()
                if self.restart_app_after_check_property:
                    return KillAppEvent(self.app)

            event = self.generate_llm_event_based_on_utg()

            if isinstance(event, RotateDevice):
                event = RotateDeviceToLandscapeEvent() if self.last_rotate_events == RotateDeviceToPortraitEvent() else RotateDeviceToPortraitEvent()
                self.last_rotate_events = event

            return event

生成基于UTG的LLM事件的方法
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**generate_llm_event_based_on_utg**
   
``generate_llm_event_based_on_utg`` 方法用于基于当前UTG生成一个LLM辅助的事件。

:参数:
   - 无

:返回:
   - 生成的事件对象。

:核心流程:
   1. 获取当前应用状态。
   2. 如果应用不在活动堆栈中，尝试启动应用。
   3. 如果应用在活动堆栈中但不在前台，尝试返回前台。
   4. 如果应用在前台，根据LLM的指导选择下一步操作。

   .. code-block:: python
       :linenos:

        def generate_llm_event_based_on_utg(self):
            current_state = self.from_state
            if current_state.get_app_activity_depth(self.app) < 0:
                start_app_intent = self.app.get_start_intent()
                return IntentEvent(intent=start_app_intent) if not self._event_trace.endswith(EVENT_FLAG_START_APP) else None

            elif current_state.get_app_activity_depth(self.app) > 0 and self.__num_steps_outside > MAX_NUM_STEPS_OUTSIDE:
                go_back_event = KeyEvent(name="BACK") if self.__num_steps_outside <= MAX_NUM_STEPS_OUTSIDE_KILL else IntentEvent(self.app.get_stop_intent())
                return go_back_event

            action, _ = self._get_action_with_LLM(current_state, self.__action_history, self.__activity_history)
            return action if action else self.__random_explore_action()

        def __random_explore_action(self):
            if self.__random_explore:
                return random.choice(self.__all_action_history)
            # If couldn't find an exploration target, stop the app
            stop_app_intent = self.app.get_stop_intent()
            return IntentEvent(intent=stop_app_intent)

查询LLM的方法
~~~~~~~~~~~~~~~~~~~~~~

**_query_llm**
   
``_query_llm`` 方法用于向LLM查询以生成事件。

:参数:
   - prompt: 提供给LLM的提示文本。
   - model_name: 使用的LLM模型名称，默认为"gpt-3.5-turbo"。

:返回:
   - LLM的响应文本。

:核心流程:
   1. 设置LLM客户端。
   2. 发送提示文本到LLM。
   3. 接收并返回LLM的响应。

   .. code-block:: python
       :linenos:

        def _query_llm(self, prompt, model_name):

            client = OpenAI()
            response = client.chat.completions.create(messages=[{"role": "user", "content": prompt}], 
            model=model_name, timeout=30)
            return response.choices[0].message.content

获取动作与LLM交互的方法
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**_get_action_with_LLM**
   
``_get_action_with_LLM`` 方法用于获取基于LLM的下一个动作。

:参数:
   - current_state: 当前应用状态。
   - action_history: 动作历史记录。
   - activity_history: 活动历史记录。

:返回:
   - 选中的动作和候选动作列表。

:核心流程:
   1. 构建包含任务描述、当前状态和历史记录的提示文本。
   2. 向LLM查询并接收响应。
   3. 解析响应以获取动作索引。
   4. 根据索引选择动作并更新历史记录。

   .. code-block:: python
       :linenos:

       def _get_action_with_LLM(self, current_state, action_history, activity_history):
    
            prompt = self._build_prompt(current_state, action_history, activity_history)
            response = self._query_llm(prompt)
            action_idx = self._parse_response(response)
            return self._select_action(action_idx, current_state, action_history, activity_history)