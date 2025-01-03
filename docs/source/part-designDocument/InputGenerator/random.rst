.. _random:

RandomPolicy
================

RandomPolicy类是随机事件生成策略的核心类。
主要负责基于当前应用状态生成随机事件。
该类提供了完整的随机事件生成策略的事件生成过程。
RandomPolicy所包含的主要方法有：

- 根据当前状态生成一个随机事件。
- 根据配置重启或重新安装应用。
- 在满足预条件的情况下，根据随机性决定是否检查性质。

随机事件生成策略的介绍
--------------------------

随机事件生成策略是一种简单有效的策略，它可以在没有明确指导路径的情况下探索应用的状态空间。
具体来说，该策略会根据当前应用的状态随机生成事件，以期达到未探索的状态或触发应用中的某些性质。
这种策略特别适用于那些没有明确测试路径或需要广泛覆盖应用状态的场景。

.. figure:: ../../images/random_flowchart.png
    :align: center

    随机探索策略的流程图

具体执行步骤如下：

步骤1：检查是否满足生成事件的条件，即事件计数是否为首次生成事件或者上一个事件是否为应用重新安装事件。

步骤2：如果满足条件，则运行初始化器并获取设备当前状态。

步骤3：判断当前状态是否为空，如果是，则等待5秒并返回一个名称为"BACK"的键事件。

步骤4：检查事件计数是否是重启应用事件数量的倍数，如果是，则根据配置决定是清除并重新安装应用还是仅仅重启应用。

步骤5：获取所有满足预条件的规则，如果存在这样的规则，则记录当前时间，并根据随机性决定是否检查性质。

步骤6：如果决定检查性质，则执行性质检查。如果检查后需要重启应用，则记录日志并返回应用杀进程事件；否则，不重启应用。

步骤7：如果因为随机性决定不检查性质，则记录日志并继续。

步骤8：基于当前应用状态生成一个随机事件。这包括将应用移至前台（如果需要），获取当前状态可能的输入事件，并添加返回键和旋转设备事件。

步骤9：从可能的事件列表中随机选择一个事件。如果选择的是旋转设备事件，则根据上次旋转事件的方向选择相反方向的旋转事件。

步骤10：返回生成的随机事件，该事件将被用于与应用的交互。

随机事件生成策略的伪代码
----------------------------


:math:`\textbf{Algorithm:} Random Event Generation`

:math:`\textbf{Input:} None`
    
:math:`\textbf{Output:} Generated Event`

.. code-block::
    :linenos:

    Function generate_event()
        current_state ← get_current_state()
        if current_state is None:
            wait(5 seconds)
            return KeyEvent(name="BACK")
        if event_count % number_of_events_that_restart_app == 0:
            if clear_and_reinstall_app:
                return ReInstallAppEvent(app)
            else:
                return KillAndRestartAppEvent(app)
        rules_to_check ← get_rules_whose_preconditions_are_satisfied()
        if len(rules_to_check) > 0:
            if random() < 0.5:
                check_property()
                if restart_app_after_check_property:
                    return KillAppEvent(app)
                return None
        event ← generate_random_event_based_on_current_state()
        return event

RandomPolicy类中的数据结构
---------------------------

1. **event_count**
   
    event_count整型，记录了已经生成的事件数量。

2. **number_of_events_that_restart_app**
   
    number_of_events_that_restart_app整型，记录了在重启应用前需要生成的事件数量。

3. **clear_and_reinstall_app**
   
    clear_and_reinstall_app布尔型，指示是否在重启应用前清除并重新安装应用。

4. **restart_app_after_check_property**
   
    restart_app_after_check_property布尔型，指示在检查性质后是否重启应用。

RandomPolicy类中的成员方法
---------------------------

生成随机事件的方法
~~~~~~~~~~~~~~~~~~~~~~

**generate_event**
   
``generate_event`` 方法用于生成一个随机事件。

:参数:
   - 无

:返回:
   - 生成的事件对象。

:核心流程:
   1. 检查是否需要运行初始化器并获取当前应用状态。
   2. 根据事件计数和设置决定是否重启应用或清除并重新安装应用。
   3. 检查是否有满足前提条件的规则，并根据随机性决定是否检查性质。
   4. 生成基于当前状态的随机事件。

   .. code-block:: python

        def generate_event(self):
            current_state = self.from_state
            if current_state is None:
                time.sleep(5)
                return KeyEvent(name="BACK")
            if self.event_count % self.number_of_events_that_restart_app == 0:
                if self.clear_and_reinstall_app:
                    return ReInstallAppEvent(self.app)
                return KillAndRestartAppEvent(self.app)
            rules_to_check = self.kea.get_rules_whose_preconditions_are_satisfied()
            if len(rules_to_check) > 0:
                if random.random() < 0.5:
                    self.check_rule_whose_precondition_are_satisfied()
                    if self.restart_app_after_check_property:
                        return KillAppEvent(self.app)
                    return None
            event = self.generate_random_event_based_on_current_state()
            return event

生成随机事件的成员方法
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**generate_random_event_based_on_current_state**
   
``generate_random_event_based_on_current_state`` 方法用于基于当前状态生成一个随机事件。

:参数:
   - 无

:返回:
   - 生成的事件对象。

:核心流程:
   1. 获取当前应用状态。
   2. 如果需要，将应用移至前台。
   3. 获取当前状态可能的输入事件。
   4. 根据随机选择生成一个事件。

   .. code-block:: python

        def generate_random_event_based_on_current_state(self):
            current_state = self.from_state
            event = self.move_the_app_to_foreground_if_needed(current_state)
            if event is not None:
                return event
            possible_events = current_state.get_possible_input()
            possible_events.append(KeyEvent(name="BACK"))
            possible_events.append(RotateDevice())
            self._event_trace += EVENT_FLAG_EXPLORE
            event = random.choice(possible_events)
            return event




