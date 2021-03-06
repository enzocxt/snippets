# -*- coding: utf-8 -*-


class DummyResource:
    def __init__(self, tag):
        self.tag = tag
        print 'Resource [%s]' % tag

    def __enter__(self):
        print '[Enter %s]: Allocate resource.' % self.tag
        return self     # 可以返回不同的对象

    def __exit__(self, exc_type, exc_value, exc_tb):
        print '[Exit %s]: Free resource.' % self.tag
        if exc_tb is None:
            print '[Exit %s]: Exited without exception.' % self.tag
        else:
            print '[Exit %s]: Exited with exception raised.' % self.tag
            return False    # 可以省略，缺省的 None 也被看作是 False
"""
DummyResource 中的 __enter__() 返回的是自身的引用，这个引用可以赋值给 as 子句中的
target 变量；返回值的类型可以根据实际需要设置为不同的类型，不必是上下文管理器对象本身。

__exit__() 方法中对变量 exc_tb 进行检测，如果不为 None，表示发生了异常，返回 False
表示需要由外部代码逻辑对异常进行处理；注意到如果没有发生异常，缺省的返回值为 None，在
布尔环境中也是被看做 False，但是由于没有异常发生，__exit__() 的三个参数都为 None，
上下文管理代码可以检测这种情况，做正常处理。
"""
def test_dummy():
    with DummyResource('Normal'):
        print '[with-body] Run without exceptions.'

    with DummyResource('With-Exception'):
        print '[with-body] Run with exception.'
        raise Exception
        print '[with-body] Run with exception. Failed to finish statement-body!'
    # 可以看到，with-body 中发生异常时with-body 并没有执行完，但资源会保证被释放掉，
    # 同时产生的异常由 with 语句之外的代码逻辑来捕获处理。


"""
上下文管理协议（Context Management Protocol）：包含方法 __enter__() 和 __exit__()，
支持该协议的对象要实现这两个方法。
上下文管理器（Context Manager）：支持上下文管理协议的对象，这种对象实现了
__enter__() 和 __exit__() 方法。上下文管理器定义执行 with 语句时要建立的运行时上下文，
负责执行 with 语句块上下文中的进入与退出操作。通常使用 with 语句调用上下文管理器，
也可以通过直接调用其方法来使用。
运行时上下文（runtime context）：由上下文管理器创建，通过上下文管理器的 __enter__() 和
__exit__() 方法实现，__enter__() 方法在语句体执行之前进入运行时上下文，__exit__() 在
语句体执行完后从运行时上下文退出。with 语句支持运行时上下文这一概念。
上下文表达式（Context Expression）：with 语句中跟在关键字 with 之后的表达式，该表达式
要返回一个上下文管理器对象。
语句体（with-body）：with 语句包裹起来的代码块，在执行语句体之前会调用上下文管
理器的 __enter__() 方法，执行完语句体之后会执行 __exit__() 方法。

with context_expression [as target(s)]:
    with-body

这里 context_expression 要返回一个 Context Manager 对象
该对象并不赋值给 as 子句中的 target(s) ，如果指定了 as 子句，会将 Context Manager 的
__enter__() 方法的返回值赋值给 target(s)。
target(s) 可以是单个变量，或者由“()”括起来的元组（不能是仅仅由“,”分隔的变量列表，必须加“()”）

Python 对一些内建对象进行改进，加入了对上下文管理器的支持，可以用于 with 语句中，
比如可以自动关闭文件、线程锁的自动获取和释放等。
"""

def show_procedure():
    filename = '/home/enzocxt/Projects/snippets/snippets.py'

    with open(filename, 'r') as inf:
        for line in inf:
            print line
            # ...more code

    # 这里使用了 with 语句，不管在处理文件过程中是否发生异常，都能保证 with 语句执行完毕后已经
    # 关闭了打开的文件句柄。如果使用传统的 try/finally 范式，则要使用类似如下代码：
    inf = open(filename, 'r')
    try:
        for line in inf:
            print line
            # ...more code
    finally:
        inf.close()

    # with 语句的执行过程
    context_manager = context_expression
    exit = type(context_manager).__exit__
    value = type(context_manager).__enter__(context_manager)
    exc = True  # True 表示正常执行，即便有异常也忽略；False 表示重新抛出异常，需要对异常进行处理
    try:
        try:
            target = value  # 如果使用了 as 子句
            # with-body     # 执行 with-body
        except:
            # 执行过程中有异常发生
            exc = False
            # 如果 __exit__ 返回 True，则异常被忽略；如果返回 False，则重新抛出异常
            # 由外层代码对异常进行处理
            if not exit(context_manager, *sys.exc_info()):
                raise
    finally:
        # 正常退出，或者通过 statement-body 中的 break/continue/return 语句退出
        # 或者忽略异常退出
        if exc:
            exit(context_manager, None, None, None)
        # 缺省返回 None, None 在布尔上下文中看作是 False

"""
1, 执行 context_expression，生成上下文管理器 context_manager
2, 调用上下文管理器的 __enter__() 方法；
   如果使用了 as 子句，则将 __enter__() 方法的返回值赋值给 as 子句中的 target(s)
3, 执行语句体 with-body
4, 不管是否执行过程中是否发生了异常，执行上下文管理器的 __exit__() 方法，
   __exit__() 方法负责执行“清理”工作，如释放资源等。
   如果执行过程中没有出现异常，或者语句体中执行了语句 break/continue/return，
   则以 None 作为参数调用 __exit__(None, None, None) ；
   如果执行过程中出现异常，则使用 sys.exc_info 得到的异常信息为参数调用
   __exit__(exc_type, exc_value, exc_traceback)
5, 出现异常时，如果 __exit__(type, value, traceback) 返回 False，则会重新抛出异常，
   让with 之外的语句逻辑来处理异常，这也是通用做法；
   如果返回 True，则忽略异常，不再对异常进行处理
"""


""" contextlib 模块
contextlib 模块提供了3个对象：装饰器 contextmanager、函数 nested 和上下文管理器 closing。
使用这些对象，可以对已有的生成器函数或者对象进行包装，加入对上下文管理协议的支持，
避免了专门编写上下文管理器来支持 with 语句。

contextmanager 用于对生成器函数进行装饰，生成器函数被装饰以后，返回的是一个上下文管理器，
其 __enter__() 和 __exit__() 方法由 contextmanager 负责提供，而不再是之前的迭代子。
被装饰的生成器函数只能产生一个值，否则会导致异常 RuntimeError；产生的值会赋值给 as 子句中的
target，如果使用了 as 子句的话。下面看一个简单的例子。
"""
from contextlib import contextmanager

@contextmanager
def demo():
    print '[Allocate resources]'
    print 'Code before yield-statement executes in __enter__'
    yield '*** contextmanager demo ***'
    print 'Code after yield-statement executes in __exit__'
    print '[Free resources]'

with demo() as value:
    print 'Assigned Value: %s' % value
"""
可以看到，生成器函数中 yield 之前的语句在 __enter__() 方法中执行，yield 之后的语句在
__exit__() 中执行，而 yield 产生的值赋给了 as 子句中的 value 变量。
需要注意的是，contextmanager 只是省略了 __enter__() / __exit__() 的编写，但并不负责
实现资源的“获取”和“清理”工作；“获取”操作需要定义在 yield 语句之前，“清理”操作需要定义在
yield 语句之后，这样 with 语句在执行 __enter__() / __exit__() 方法时会执行这些语句
以获取/释放资源，即生成器函数中需要实现必要的逻辑控制，包括资源访问出现错误时抛出适当的异常。
"""

""" 函数 nested
nested 可以将多个上下文管理器组织在一起，避免使用嵌套 with 语句。
with nested(A(), B(), C()) as (X, Y, Z):
     # with-body code here
类似于：
with A() as X:
    with B() as Y:
        with C() as Z:
             # with-body code here
需要注意的是，发生异常后，如果某个上下文管理器的 __exit__() 方法对异常处理返回 False，
则更外层的上下文管理器不会监测到异常。
"""

""" 上下文管理器 closing
closing 的实现如下：
"""
class closing(object):
    # help doc here
    def __init__(self, thing):
        self.thing = thing
    def __enter__(self):
        return self.thing
    def __exit__(self, *exc_info):
        self.thing.close()

# 上下文管理器会将包装的对象赋值给 as 子句的 target 变量，同时保证打开的对象在 with-body
# 执行完后会关闭掉。closing 上下文管理器包装起来的对象必须提供 close() 方法的定义，
# 否则执行时会报 AttributeError 错误。
class ClosingDemo(object):
    def __init__(self):
        self.acquire()
    def acquire(self):
        print 'Acquire resources.'
    def free(self):
        print 'Clean up any resources acquired.'
    def close(self):
        self.free()

with closing(ClosingDemo()):
    print 'Using resources'

"""
closing 适用于提供了 close() 实现的对象，比如网络连接、数据库连接等，也可以在自定义类时
通过接口 close() 来执行所需要的资源“清理”工作。
"""
