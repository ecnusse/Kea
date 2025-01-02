带状态的测试
========================

带状态的测试是一种软件测试方法，专注于系统在不同状态下的行为和响应。
其原理基于状态管理和状态转移，通过设计测试用例来覆盖各种状态及其转换，以确保系统在不同条件下的正确性和一致性。
此方法适合应用于需要保持状态前后一致的应用程序，通过设计带状态的测试用例，
确保系统在各种状态下正常运行，从而增强软件的可靠性和用户体验。

在移动应用中，一些功能可以根据特定的输入或操作从一个状态转换到另一个状态。因此，需要额外的数据结构来支持这一点。

在 Kea 中，当你编写需要记录状态信息的性质时，可以使用带状态的测试。如以下代码所示，当你想在设备上进行文件或文件夹的相关操作时，例如创建文件、删除文件或重命名文件。

你可以编写以下代码：

.. code:: Python

    _files = Kea.Bundle("files")

Bundle 类包含以下函数：

* add(value: str)

向当前的 Bundle 对象内添加一个新值。

.. code-block:: Python

    self._files.add(file_name)

* delete(value: str)

从当前的 Bundle 对象中删除一个值。

.. code-block:: Python

    self._files.delete(selected_file_name)

* update(value: str, new_value: str)

将当前对象中 ``value`` 的值更新为 ``new_value``

.. code-block:: Python

    self._files.update(file_name, new_name)

* get_all_data()

该函数会返回当前 Bundle 对象存储的值列表。

.. code-block:: Python

    self._files.get_all_data()

* get_random_value(value_len: int = 10)

该函数会随机生成一个值并返回。因此，你可以在使用 ``add`` 和 ``update`` 函数之前调用它。

.. code-block:: Python

    file_name = self._files.get_random_value()
    self._files.add(file_name)

* get_random_data()

该函数会从当前 Bundle 对象存储的值中随机选择一个值并返回。因此，你可以在使用 delete 和 update 函数之前调用它。

.. code-block:: Python

    file_name = self._files.get_random_data()
    self._files.delete(selected_file_name)

接下来是一个完整的示例，展示了如何在定义性质时使用 Kea 的状态测试。这个示例将展示如何在应用程序
`Amaze <https://github.com/TeamAmaze/AmazeFileManager>`_ 中使用状态测试， ``Amaze`` 是一个文件管理应用，
允许用户在设备上操作文件或文件夹。这些性质是为了测试文件系统的数据操作是否存在错误而定义的。
在这种情况下，带状态的测试至关重要，你可以使用 ``Bundle`` 来存储 Kea 创建的所有文件夹，并在整个测试过程中对它们进行操作。

首先，你可以定义一个 ``create_file_should_exist`` 性质。该性质的实现步骤如下：1. 返回到主目录。 2.创建一个文件。 3.检查新文件是否存在。
这个性质可以确保在创建文件后，文件确实存在于预期的位置。

.. figure:: ../images/CreateFile.png
        :align: center

        创建文件夹截图

.. code-block:: Python

        @precondition(lambda self: d(resourceId="com.amaze.filemanager:id/sd_main_fab").exists() and
                                   not d(textContains = "SDCARD").exists())
        @rule()
        def create_file_should_exist(self):
            d.swipe_ext("down", scale=0.9)
            d(description="Navigate up").click()
            d(resourceId="com.amaze.filemanager:id/design_menu_item_text", textContains="Internal Storage").click()
            d(resourceId="com.amaze.filemanager:id/sd_main_fab").click()
            d(resourceId="com.amaze.filemanager:id/sd_label", text="Folder").click()
            file_name = self._files.get_random_value()
            d.send_keys(file_name, clear=True)
            d(resourceId="com.amaze.filemanager:id/md_buttonDefaultPositive").click()
            self._files.add(file_name)
            d(scrollable=True).scroll.to(resourceId="com.amaze.filemanager:id/firstline", text=file_name)
            assert d(text=file_name).exists()

接下来, 你可以定义一个 ``change_filename_should_follow`` 性质。 该性质的实现步骤如下：返回到主目录，随机选择一个文件，改变它的名称，并检查原来名称的文件是否消失并且新名称的文件是否存在。

..  figure:: ../images/RenameFile.png
        :align: center

        重命名文件夹截图

.. code-block:: Python

        @precondition(lambda self:  self._files.get_all_data() and
                                    d(resourceId="com.amaze.filemanager:id/sd_main_fab").exists() and
                                    not d(resourceId="com.amaze.filemanager:id/action_mode_close_button").exists())
        @rule()
        def change_filename_should_follow(self):
            d.swipe_ext("down", scale=0.9)
            d(description="Navigate up").click()
            d(resourceId="com.amaze.filemanager:id/design_menu_item_text", textContains="Internal Storage").click()
            file_name = self._files.get_random_data()
            new_name = self._files.get_random_value()
            d(scrollable=True).scroll.to(resourceId="com.amaze.filemanager:id/firstline", text=file_name)
            selected_file = d(resourceId="com.amaze.filemanager:id/firstline", text=file_name)
            selected_file.right(resourceId="com.amaze.filemanager:id/properties").click()
            d(text="Rename").click()
            d.send_keys(new_name, clear=True)
            d(resourceId="com.amaze.filemanager:id/md_buttonDefaultPositive").click()
            self._files.update(file_name, new_name)
            d.swipe_ext("down", scale=0.9)
            d(resourceId="com.amaze.filemanager:id/home").click()
            d(scrollable=True).scroll.to(resourceId="com.amaze.filemanager:id/firstline", text=new_name)
            assert d(text=new_name).exists()
            d.swipe_ext("down", scale=0.9)
            d(resourceId="com.amaze.filemanager:id/home").click()
            d(scrollable=True).scroll.to(resourceId="com.amaze.filemanager:id/firstline", text=file_name)
            assert not d(text=file_name).exists()

最后, 你可以定义一个 ``del_file_should_disappear`` 性质。返回到主目录，删除一个文件，并检查该文件是否存在。

..  figure:: ../images/DelFile.png
        :align: center

        删除文件夹截图

.. code-block:: Python

        @precondition(lambda self:  self._files.get_all_data() and
                                    d(resourceId="com.amaze.filemanager:id/sd_main_fab").exists() and
                                    not d(resourceId="com.amaze.filemanager:id/action_mode_close_button").exists())
        @rule()
        def del_file_should_disappear(self):
            d.swipe_ext("down", scale=0.9)
            d(description="Navigate up").click()
            d(resourceId="com.amaze.filemanager:id/design_menu_item_text", textContains="Internal Storage").click()
            file_name = self._files.get_random_data()
            d(scrollable=True).scroll.to(resourceId="com.amaze.filemanager:id/firstline", text = file_name)
            selected_file = d(resourceId="com.amaze.filemanager:id/firstline", text = file_name)
            selected_file_name = selected_file.get_text()
            selected_file.right(resourceId="com.amaze.filemanager:id/properties").click()
            d(text="Delete").click()
            d(resourceId="com.amaze.filemanager:id/md_buttonDefaultPositive").click()
            self._files.delete(selected_file_name)
            d.swipe_ext("down", scale=0.9)
            d(resourceId="com.amaze.filemanager:id/home").click()
            d(scrollable=True).scroll.to(resourceId="com.amaze.filemanager:id/firstline", text=file_name)
            assert not d(text=selected_file_name).exists()
