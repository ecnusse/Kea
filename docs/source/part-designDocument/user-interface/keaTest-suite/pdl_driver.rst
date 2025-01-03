PDL 驱动
======================

本部分旨在解释 Kea 的性质定义语言驱动 PDL 是如何设计及实现的。

PDL 驱动的功能设计
---------------------

PDL 驱动是在基于性质的测试中，用户与设备在执行性质时与设备交互的驱动。
PDL 驱动有安卓设备的 PDL 驱动（基于uiautomator2），鸿蒙设备的 PDL 驱动（基于hmdriver2）

.. note:: 

    PDL 驱动设计参考了 uiautomator2 和 hmdriver2

    uiautomator2: https://github.com/openatx/uiautomator2

    hmdriver2: https://github.com/codematrixer/hmdriver2

PDL驱动的使用语法是 ``d(Selector(**kwargs)).attr(args)`` 。其中 ``Selecotor(**kwargs)`` 是控件选择器，
控件选择器通过字典的方式指定控件的属性，如安卓中的 resourceId, className，鸿蒙中的 id， bundlename等。attr
是对选定控件的操作，包括click、longClick等操作。 ``attr(args)`` 中的 ``args`` 为传入方法的参数。如在
``input_text("Hello")`` 中传入要输入的字符串 "Hello"。

我们的PDL驱动实际上是kea与对应自动化测试工具(uiautomator2、hmdriver2)的中间层，语法与目标的测试工具一致，
主要用于做一些额外的操作，如保存当前事件、截图等，以方便kea访问到对应的操作数据，方便生成错误报告等。

安卓设备的 PDL 驱动的实现
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

安卓设备的PDL驱动通过uiautomator2实现。主要用于让用户编写的性质和应用进行交互。

安卓的PDL驱动继承于uiautomator2的Driver类，部分安卓PDL的python风格简化代码实现示意如下：

.. code-block:: python

    class Android_PDL_Driver(Uiautomator2.Driver):  

        def __call__(self, **kwargs: Any) -> Ui:
            return Ui(self, Selector(**kwargs), droidbot=self.droidbot)

        def set_droidbot(self, droidbot:DroidBot):
            self.droidbot = droidbot

        ...

    class Ui(Uiautomator2.UiObject):
        def __init__(self, session:Android_PDL_Driver, selector: Selector, droidbot:DroidBot):
            super().__init__(session, selector)
            self.droidbot=droidbot

        def click(self, offset=None):
            self.droidbot.device.save_screenshot_for_report(event_name="click", event = self)
            print(f"Property Action: click({str(self.selector)})")
            super().click(offset)
        
        ...
            
        def child(self, **kwargs):
            return Ui(self.session, self.selector.clone().child(**kwargs), self.droidbot)
        
        def sibling(self, **kwargs):
            return Ui(self.session, self.selector.clone().sibling(**kwargs), self.droidbot)

PDL的核心功能的解析如下：

.. code-block::

    1. 使 PDL 能按 d(Selectors(**kwargs)).attr(*args) 的方式调用：
       
        def __call__(self, **kwargs: Any) -> Ui:
            return Ui(self, Selector(**kwargs), droidbot=self.droidbot)
        
        python的函数是一等对象，定义driver对象的 __call__ 魔术方法可以让对象可以通过函数的方式调用，完成形如d(**kwargs)的调用方法。
        
        UI是uiautomator2中的UI对象类，可以调用 .attrs() 方法。通过定义驱动的 __call__ 返回一个UI对象可以完成如此的调用。
    
    2. 使PDL驱动能和kea主体的其他功能进行资源共享：

        kea调用本PDL类的set_droidbot方法设置Droidbot，让本类可以访问droidbot。以此，需要的资源可以通过调用droidbot的方法返回给kea。
    
    3. 发送资源到kea。
       
        def click(self, offset=None):
            self.droidbot.device.save_screenshot_for_report(event_name="click", event = self)

        在执行点击操作的时候，调用droidbot中的对应方法保存截图和当前的事件操作。其他的控件操作方法定义类似。
    
    4. 让PDL能使用uiautomator2中的.child等相对控件获取方法。
        
        定义 child、 sibling方法内容，根据功能返回对应的相对控件。

鸿蒙设备的 PDL 驱动实现
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

鸿蒙设备的PDL驱动通过hmdriver2实现。主要用于让用户编写的性质和应用进行交互。

鸿蒙的PDL驱动继承于hmdriver2的Driver类，部分鸿蒙PDL的python风格简化代码实现示意如下：

.. code-block:: python

    class HarmonyOS_PDL_Driver(hmdriver2.Driver):

        def __call__(self, **kwargs: Any) -> Ui:
            return Ui(self, **kwargs)

        def set_droidbot(self, droidbot:Droidbot):
            self.droidbot = droidbot


    class Ui(hmdriver2.UiObject):
        def __init__(self, session:HarmonyOS_PDL_Driver, **kwargs) -> None:
            client = session._client
            droidbot = session.droidbot
            self.droidbot = droidbot
            super().__init__(client, **kwargs)

        def click(self, offset=None):
            self.droidbot.device.save_screenshot_for_report(event_name="click", event = self)
            super().click()
            

.. code-block::

    1. 使 PDL 能按 d(Selectors(**kwargs)).attr(*args) 的方式调用：
       
        def __call__(self, **kwargs: Any) -> Ui:
            return Ui(self, **kwargs)
        
        python的函数是一等对象，定义driver对象的 __call__ 魔术方法可以让对象可以通过函数的方式调用，完成形如d(**kwargs)的调用方法。
        
        UI是hmdriver2中的UI对象类，可以调用 .attrs() 方法。通过定义驱动的 __call__ 返回一个UI对象可以完成如此的调用。
    
    2. 使PDL驱动能和kea主体的其他功能进行资源共享：

        kea调用本PDL类的set_droidbot方法设置Droidbot，让本类可以访问droidbot。以此，需要的资源可以通过调用droidbot的方法返回给kea。
    
    3. 发送资源到kea。
       
        def click(self, offset=None):
            self.droidbot.device.save_screenshot_for_report(event_name="click", event = self)

        在执行点击操作的时候，调用droidbot中的对应方法保存截图和当前的事件操作。其他的控件操作方法定义类似。