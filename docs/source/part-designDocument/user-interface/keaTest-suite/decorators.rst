性质装饰器
=============================

本部分旨在解释 Kea 的性质定义装饰器是如何设计及实现的。

功能说明与功能设计
---------------------

在KeaTest中，使用装饰器定义性质。装饰器的作用是对函数本身进行修改。在Kea中，用户的初始化、前置条件、主路径函数都是一个函数，
我们使用装饰器获取函数体，并对这个函数体进行标记。由于python中函数为一等对象，我们使用装饰器获取函数体后可以动态地往这个函数对象中
设置属性，我们根据不同的装饰器，设置不同的MARKER属性标记。在Kea加载性质的时候，我们读取如下的数据结构，
并将如下的数据结构通过KeaTestElements类进行读取，并转换为方便Kea读取和处理的数据结构：KeaTestElements。



.. _decorators-keaTestElements:

.. figure:: ../../../images/decorators-keaTestElements.png
    :align: center

    从用户自定义KeaTest到运行时KeaTestElements的转换

性质的定义
---------------------------------

下述的@rule和@precondition装饰器将用户定义的一条性质封装在数据结构Rule中，并对这个性质的函数进行使用RULE_MARKER进行标记。

以下是Rule数据数据结构的定义。precondition用于存放一个函数对象，存储一个计算前置条件的函数。function用于存储这条性质的交互场景(interaction scenario)。

.. code-block:: python

    @attr.s(frozen=True)
    class Rule:    
        # `preconditions` denotes the preconditions annotated with `@precondition`
        preconditions:Callable = attr.ib()  

        # `function` denotes the function of @Rule. 
        # This function includes the interaction scenario and the assertions (i.e., the postconditions)
        function:Callable = attr.ib()

@rule装饰器用于定义一条性质。其中，RULE_MARKER为一个常量。

:参数:
    - ``f: Callable[[Any], None]`` : 一个交互场景函数对象

:返回:
    - ``Callable[[Any], None]`` : 被RULE_MARKER标记后已解析Rule的函数对象


.. code-block:: python

    def rule() -> Callable:
        def accept(f):
            precondition = getattr(f, PRECONDITIONS_MARKER, ())
            rule = Rule(function=f, preconditions=precondition)

            def rule_wrapper(*args, **kwargs):
                return f(*args, **kwargs)

            setattr(rule_wrapper, RULE_MARKER, rule)
            return rule_wrapper

        return accept

@precondition前提条件指定了性质何时可以被执行。一个性质可以有多个前提条件，每个前提条件由 `@precondition` 指定。其中，
PRECONDITIONS_MARKER为一个常量。

:参数:
    - ``precond: Callable[[Any], bool]`` : 一个返回布尔值的已经被@rule装饰过的函数对象

:返回:
    - ``Callable[[Any], bool]`` : 被RULE_MARKER标记后已解析前置条件的函数

.. code-block:: python

    def precondition(precond: Callable[[Any], bool]) -> Callable:
        def accept(f):
            def precondition_wrapper(*args, **kwargs):
                return f(*args, **kwargs)

            rule:"Rule" = getattr(f, RULE_MARKER, None)
            if rule is not None:
                new_rule = rule.evolve(preconditions=rule.preconditions + (precond,))
                setattr(precondition_wrapper, RULE_MARKER, new_rule)
            else:
                setattr(
                    precondition_wrapper,
                    PRECONDITIONS_MARKER,
                    getattr(f, PRECONDITIONS_MARKER, ()) + (precond,),
                )
            return precondition_wrapper

        return accept

初始化函数的定义
------------------

@initializer定义一个初始化函数，用于应用的初始化，如跳过新手教程等。
下述的@initializer装饰器将用户定义的一条性质封装在数据结构Initializer中，并对这个性质的函数进行使用INITIALIZER_MARKER进行标记。

以下是Initializer数据结构的定义。function用于存放一个函数对象，为初始化时要执行的一系列操作。

.. code-block:: python

    @attr.s()
    class Initializer: 
        # `function` denotes the function of `@initializer.
        function:Callable = attr.ib()

@initializer装饰器用于定义一个初始化函数，其中，INITIALIZER_MARKER是一个常量。

:参数:
    - ``f: Callable[[Any], None]`` : 定义了初始化事件的初始化函数对象

:返回:
    - ``Callable[[Any], None]`` : 被INITIALIZER_MARKER标记的初始化函数对象

.. code-block:: python

    def initializer():
        def accept(f):
            def initialize_wrapper(*args, **kwargs):
                return f(*args, **kwargs)

            initializer_func = Initializer(function=f)
            setattr(initialize_wrapper, INITIALIZER_MARKER, initializer_func)
            return initialize_wrapper

        return accept

主路径函数的定义
---------------------

主路径指定了一系列事件，从应用起始页执行这些事件会将应用引到至性质的起始状态（满足前置条件的页面）。
下述的@mainPath装饰器将用户定义的一条性质封装在数据结构MainPath中，并对这个性质的函数进行使用MAINPATH_MARKER进行标记。

以下是MainPath数据结构的定义。function用于存放用户定义的mainPath函数对象，path为对这个函数进行源代码处理后获取的详细路径步骤，
为一个存储了主路径中各个步骤的源代码的列表。

.. code-block:: python

    @attr.s()
    class MainPath:
        
        # `function` denotes the function of `@mainPath.
        function:Callable = attr.ib()

        # the interaction steps (events) in the main path
        path: List[str] = attr.ib()  


@mainPath装饰器将用户定义的一条性质封装在数据结构MainPath中，其中，MAINPATH_MARKER是一个常量。

:参数:
    - ``f: Callable[[Any], None]`` : 定义了主路径事件的函数对象

:返回:
    - ``Callable[[Any], None]`` : 被MAINPATH_MARKER标记的初始化函数对象

.. code-block:: python

    def mainPath():
        def accept(f):
            def mainpath_wrapper(*args, **kwargs):
                source_code = inspect.getsource(f)
                code_lines = [line.strip() for line in source_code.splitlines() if line.strip()]
                code_lines = [line for line in code_lines if not line.startswith('def ') and not line.startswith('@') and not line.startswith('#')]
                return code_lines

            main_path = MainPath(function=f, path=mainpath_wrapper())
            setattr(mainpath_wrapper, MAINPATH_MARKER, main_path)
            return mainpath_wrapper

        return accept