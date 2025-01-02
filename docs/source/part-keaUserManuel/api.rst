.. _pdl_api:

应用性质描述语言接口
==========================

应用性质描述语言（PDL）是Kea与被测试应用交互的方式，用户可通过接口的调用来实现与被测移动应用的交互。

用户界面交互事件
-----------------

.. note::

   目前，kea的性质描述语言底层通过 `uiautomator2 <https://github.com/openatx/uiautomator2>`_ 作为交互工具，来进行与移动设备的交互。

例如，要向应用程序发送点击事件，你可以使用以下代码：

.. code-block:: Python

   d(resourceId="player_playback_button").click()


``d`` 是 uiautomator2 的驱动。

``resourceId`` 设置组件的编号，用于选择器定位组件。

``click()`` 表示向该组件发送点击事件。

下面是一些常用的交互事件:

* click

   .. code-block:: Python

      d(text="OK").click()
  
* long_click

   .. code-block:: Python

      d(text="OK").long_click()

* edit text

   .. code-block:: Python

      d(text="OK").set_text("text")

* rotate device

   .. code-block:: Python

      d.rotate("l") # or left
      d.rotate("r") # or right

* press [key]

   .. code-block:: Python

      d.press("home")
      d.press("back")

在定位组件时，可以使用以下选择器。

选择器
---------------------

选择器用于在用户界面中识别特定的组件，其支持以下参数：

*  ``text``, ``textContains``, ``textMatches``, ``textStartsWith``
*  ``className``, ``classNameMatches``
*  ``description``, ``descriptionContains``, ``descriptionMatches``, ``descriptionStartsWith``
*  ``checkable``, ``checked``, ``clickable``, ``longClickable``
*  ``scrollable``, ``enabled``, ``focusable``, ``focused``, ``selected``
*  ``packageName``, ``packageNameMatches``
*  ``resourceId``, ``resourceIdMatches``
*  ``index``, ``instance``  


样例
---------------------------

.. code-block:: python

   # 选择text值为 "More Options" 的控件并点击它。
   d(text='More Options').click()

   # 在一个选择器中使用多个参数。
   # 选择具有text值为 "Clock" 和类名为 "android.widget.TextView" 的控件并点击它。
   d(text='Clock', className='android.widget.TextView').long_click()

   # 选择具有资源编号为 "com.example/input_box" 的控件，并将其文本值设置为 "Hello world"。
   d(resourceId="com.example/input_box").set_text("Hello world")
