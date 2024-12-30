性质定义教程
================================

在本教程中，你将学习如何使用 Kea 编写应用性质并进行测试。

在移动应用中，性质定义了应用的预期行为。如果应用违反了该性质，则意味着发现了一个错误。

用户所定义的应用功能性质由三个关键组件组成。 **<P, I, Q>**, (1) *P* 是一个前置条件, 
(2) *I* 是一个交互场景，定义了如何执行应用功能, 
(3) *Q* 是一个后置条件，定义了预期的行为。

Kea 给用户提供 ``@initializer()`` 帮助用户定义初始化函数，让应用能够跳过欢迎页面或登录页面。

在 Kea 中，性质是通过应用 ``@rule()`` 这样一个性质函数上的装饰器来定义的。

要定义性质的前置条件，用户可以在 ``@rule()`` 装饰的函数上，使用装饰器 ``@precondition()``。

后置条件则在 ``@rule()`` 装饰的函数内部使用 ``assert`` 来完成定义。

对于移动应用，用户可以从多个途径获取应用性质，例如应用的规范、应用的文档、应用的测试用例、应用的错误报告等。

让我们从几个简单的例子开始，介绍如何获取一个性质，如何在 Kea 中编写该性质，以及如何通过 Kea 测试该性质。

从应用错误报告中获取应用性质
---------------------------------------------

以下这个例子将展示如何从应用 `OmniNotes <https://github.com/federicoiosue/Omni-Notes/>`_ 中获取一个性质。

`OmniNotes <https://github.com/federicoiosue/Omni-Notes/>`_ 是一个用于记录和管理笔记的应用。

本样例来自该应用的错误报告 `#634 <https://github.com/federicoiosue/Omni-Notes/issues/634>`_, 用户表示，当他删除一个标签时，其他共享相同前缀的标签也被删除。

然后，从这个错误报告中，可以得到一下应用性质：

在删除标签后，标签应该成功移除，笔记内容应保持不变。

根据错误报告，你可以得到一个这样的应用性质：

- **P (前置条件)**: 应该有标签存在。
- **I (交互场景)**: 从标签列表中移除某个标签。
- **Q (后置条件)**: 指定的标签被删除，并且其余文本内容保持不变。

接下来，让我们在Kea中使用性质描述语言定义该性质。


.. code-block:: Python

    @precondition(lambda self: d(resourceId="it.feio.android.omninotes:id/menu_tag").exists() and
                   "#" in d(resourceId="it.feio.android.omninotes:id/detail_content").info["text"]
                   )
    @rule()
    def rule_remove_tag_from_note_shouldnot_affect_content(self):
        # get the text from the note's content
        origin_content = d(resourceId="it.feio.android.omninotes:id/detail_content").info["text"]
        # click to open the tag list
        d(resourceId="it.feio.android.omninotes:id/menu_tag").click()
        # select a tag to remove
        selected_tag = random.choice(d(className="android.widget.CheckBox",checked=True))
        select_tag_name = "#"+ selected_tag.right(resourceId="it.feio.android.omninotes:id/md_title").info["text"].split(" ")[0]
        selected_tag.click()
        # click to uncheck the selected tag
        d(text="OK").click()
        # get the updated content after removing the tag
        new_content = d(resourceId="it.feio.android.omninotes:id/detail_content").info["text"].strip().replace("Content", "")
        # get the expected content after removing the tag
        origin_content_exlude_tag = origin_content.replace(select_tag_name, "").strip()
        # the tag should be removed in the content and the updated content should be the same as the expected content
        assert not d(textContains=select_tag_name).exists() and new_content == origin_content_exlude_tag

``@precondition`` 装饰器定义了该性质应当开始被测试的状态节点。
代码中， ``d(resourceId="it.feio.android.omninotes:id/menu_tag").exists()`` 检查了是否标签按钮存在于界面内，
``"#" in d(resourceId="it.feio.android.omninotes:id/detail_content").info["text"]`` 检查了是否笔记内容中存在“#”字符。


``@rule()`` 装饰器定义了应用性质函数。
在本段代码中，交互场景为执行移除标签的操作。

后置条件则由 ``assert`` 语句来完成定义。
这里，Kea检查是否指定的标签被删除并且保持其余文本不变。

像这样一条性质就是应该由 `OmniNotes <https://github.com/federicoiosue/Omni-Notes/>`_ 应用所遵循的。

此外，用户还可以定义一个初始化函数，在测试性质之前设置应用的初始状态。

为了实现该功能，用户可以使用一个 ``@initializer()`` 装饰器来定义一个初始化函数并且写一些UI操作指令，来引导应用完成初始化操作:

.. code:: Python

    @initializer()
    def set_up(self):
        for _ in range(5):
            d(resourceId="it.feio.android.omninotes:id/next").click()
        d(resourceId="it.feio.android.omninotes:id/done").click()
        if d(text="OK").exists():
            d(text="OK").click()

在这里，上述代码可以自动通过UI操作来跳过 `OmniNotes <https://github.com/federicoiosue/Omni-Notes/>`_ 的欢迎页面。
你可以使用 ``@initializer()`` 装饰器来定义任意应用的初始化函数。这样，Kea 会在测试应用性质之前执行该初始化函数。
这样可以确保在每次测试开始时，应用都处于预期的初始状态。

.. tip:: 

    这个功能可以用来在测试应用性质之前设置应用程序的初始状态。
    例如，可以使用此功能进行登录、向应用程序添加数据等。
    如果不需要设置应用程序的初始状态，可以跳过此步骤。

此外，如果用户想使用主路径引导探索策略，需要使用 ``@mainPath()`` 装饰器定义一个函数来设置一个主路径函数。

为了给该应用完成该步骤，可以使用以下代码来定义主路径。

.. code:: Python

    @mainPath()
    def test_main(self):
        d(resourceId="it.feio.android.omninotes.alpha:id/fab_expand_menu_button").long_click()
        d(resourceId="it.feio.android.omninotes.alpha:id/detail_content").click()
        d(resourceId="it.feio.android.omninotes.alpha:id/detail_content").set_text("read a book #Tag1")
        d(description="drawer open").click()
        d(resourceId="it.feio.android.omninotes.alpha:id/note_content").click()

上述代码可以引导 Kea 在 Omninotes 中创建一条内容为“read a book #Tag1”的笔记。

.. tip::

    在主路径定义部分，只能使用 UI 操作命令来完成定义；
    该函数目前不支持其他 Python 语句，例如 for 循环。
    但我们认为这种方法足以实现主路径的功能。

太棒了！到此，你已经学会了如何使用性质描述语言从错误报告中提取并定义一个应用性质。

要测试这个性质，用户需要将其放入定义的一个类中，该类继承自 ``KeaTest`` 类。

.. code:: Python
    
    from kea.main import *

    class Test(KeaTest):

        @initialize()
        def set_up(self):
            for _ in range(5):
                d(resourceId="it.feio.android.omninotes:id/next").click()
            d(resourceId="it.feio.android.omninotes:id/done").click()
            if d(text="OK").exists():
                d(text="OK").click()

        @mainPath()
        def test_main(self):
            d(resourceId="it.feio.android.omninotes.alpha:id/fab_expand_menu_button").long_click()
            d(resourceId="it.feio.android.omninotes.alpha:id/detail_content").click()
            d(resourceId="it.feio.android.omninotes.alpha:id/detail_content").set_text("read a book #Tag1")
            d(description="drawer open").click()
            d(resourceId="it.feio.android.omninotes.alpha:id/note_content").click()

        @precondition(lambda self: d(resourceId="it.feio.android.omninotes:id/menu_tag").exists() and
                    "#" in d(resourceId="it.feio.android.omninotes:id/detail_content").info["text"]
                    )
        @rule()
        def rule_remove_tag_from_note_shouldnot_affect_content(self):
            # get the text from the note's content
            origin_content = d(resourceId="it.feio.android.omninotes:id/detail_content").info["text"]
            # click to open the tag list
            d(resourceId="it.feio.android.omninotes:id/menu_tag").click()
            # select a tag to remove
            selected_tag = random.choice(d(className="android.widget.CheckBox",checked=True))
            select_tag_name = "#"+ selected_tag.right(resourceId="it.feio.android.omninotes:id/md_title").info["text"].split(" ")[0]
            selected_tag.click()
            # click to uncheck the selected tag
            d(text="OK").click()
            # get the updated content after removing the tag
            new_content = d(resourceId="it.feio.android.omninotes:id/detail_content").info["text"].strip().replace("Content", "")
            # get the expected content after removing the tag
            origin_content_exlude_tag = origin_content.replace(select_tag_name, "").strip()
            # the tag should be removed in the content and the updated content should be the same as the expected content
            assert not d(textContains=select_tag_name).exists() and new_content == origin_content_exlude_tag

在这里，需要在继承自 ``KeaTest`` 类的 ``Test`` 类中编写定义该性质。

我们将这个性质脚本文件 ``example_mainpath_property.py`` 放在 ``example`` 目录中。
用户可以通过运行以下命令来测试应用的该性质。

.. code:: console

    kea -f example/example_mainpath_property.py -a example/omninotes.apk

当你尝试测试这个性质时，你可能会迅速发现两个新的错误，这些错误违反了该性质。
然后，你可以撰写相应的错误报告并提交给应用程序的开发人员。这两个错误目前都已被开发人员修复。

你可以查看这两个错误的报告：

1. `Bug Report: Note tag cannot be removed <https://github.com/federicoiosue/Omni-Notes/issues/942>`_.


2. `Bug Report: Deleting One Tag in a Note Affects Another Tag in the Same Note <https://github.com/federicoiosue/Omni-Notes/issues/949>`_.

从指定应用程序功能中提取性质
---------------------------------------------
接下来是一个完整的示例，展示了如何从应用 `Amaze <https://github.com/TeamAmaze/AmazeFileManager>`_ 的功能中提取性质。

`Amaze <https://github.com/TeamAmaze/AmazeFileManager>`_ 是一个文件管理应用程序。它提供了简洁直观的用户界面，允许用户轻松浏览、管理和操作文件。

在 Amaze 中，你可以创建一个文件夹，并且在创建后新文件夹应该存在。因此，你可以定义一个性质 ``create_folder_should_exist``。
这意味着当你想要创建一个文件夹时，它应该能够被成功创建。


你任然需要使用 ``@rule()`` 和 ``@precondition()`` 来完成应用性质的定义。
在这个样例中，前置条件 *P* 是创建新文件夹的按钮需要存在，并处于能够创建文件夹的界面上。
交互场景 *I* 是一些创建文件夹的操作事件序列。
最后，后置条件 *Q* 是检查新创建的文件夹是否存在。

.. code:: Python

    @precondition(lambda self: d(resourceId="com.amaze.filemanager:id/sd_main_fab").exists() and
                               not d(textContains = "SDCARD").exists())
    @rule()
    def create_folder_should_exist(self):
        d(resourceId="com.amaze.filemanager:id/sd_main_fab").click()
        d(resourceId="com.amaze.filemanager:id/sd_label", text="Folder").click()
        file_name = self._files.get_random_value()
        d.send_keys(file_name, clear=True)
        d(resourceId="com.amaze.filemanager:id/md_buttonDefaultPositive").click()
        d(scrollable=True).scroll.to(resourceId="com.amaze.filemanager:id/firstline", text=file_name)
        assert d(text=file_name).exists()

太好了！你已经学会了如何从应用程序功能中编写应用性质。

.. note::

    用户可以在一个 ``.py`` 文件中编写一个应用程序的单个性质或多个性质。也可以将多个性质写在多个 .py 文件中。
    如果选择第一种方法，用户需要确保在一个 .py 文件中最多只有一个 ``@initializer()`` 和一个 ``@mainPath()``，
    同时有多个 ``@rule()`` 和 ``@precondition()`` 来对应不同的性质。测试用例的结构如下图所示（请根据需要添加图像或示例代码）。