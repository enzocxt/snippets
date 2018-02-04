# -*- coding: utf-8 -*-

import logging


'''
教程：
http://www.jianshu.com/p/feb86c06c4f4
http://python.jobbole.com/81666/
日志级别：DEBUG, INFO, WARNING, ERROR, CRITICAL

几个比较重要的概念： Logger, Handler, Formatter, Filter
Logger 记录器， 保留了应用程序代码能直接使用的借口
Handler 处理器， 将（记录器产生的）日志记录发送至合适的目的地
Filter 过滤器，提供了更好的粒度控制，它可以决定输出哪些日志记录
Formatter 格式化器，指明了最终输出中日志记录的布局

使用接口之前必须创建 Logger 实例，即创建一个记录器，如果没有显式的进行创建，
则默认创建一个root logger，并应用默认的日志级别(WARN)，
处理器Handler (StreamHandler，即将日志信息打印输出在标准输出上)，
和格式化器Formatter(默认的格式即为第一个简单使用程序中输出的格式)。
'''
handler_name = "test"
logger = logging.getLogger('test')
logger.setLevel(logging.ERROR)      # 设置日志级别为 ERROR， 即只有日志级别大于等于 ERROR 的日志才会输出
logger.addHandler(handler_name)     # 为 Logger 实例增加一个处理器
logger.removeHandler(handler_name)  # 为 Logger 实例删除一个处理器

# logging.basicConfig(filename='logger.log', level=logging.INFO)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-4s %(levelname)-4s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='logger.log',
                    filemode='w')

# 创建 StreamHandler
console = logging.StreamHandler(stream=None)
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)
# 创建 FileHandler
fh = logging.FileHandler(filename, mode='a', encoding=None, delay=False)
# FOrmatter 格式化器
# 使用Formatter对象设置日志信息最后的规则、结构和内容，默认的时间格式为%Y-%m-%d %H:%M:%S
# fmt是消息的格式化字符串，datefmt是日期字符串。如果不指明fmt，将使用'%(message)s'。
# 如果不指明datefmt，将使用ISO8601日期格式
formatter = logging.Formatter(fmt=None, datefmt=None)
# Filter 过滤器
# Handlers 和 Loggers 可以使用 Filters 来完成比级别更复杂的过滤。
# Filter 基类只允许特定 Logger 层次以下的事件。例如用 ‘A.B’ 初始化的 Filter 允许 Logger
# ‘A.B’, ‘A.B.C’, ‘A.B.C.D’, ‘A.B.D’等记录的事件，logger‘A.BB’, ‘B.A.B’ 等就不行。
# 如果用空字符串来初始化，所有的事件都接受。
flt = logging.Filter(name='')
# Logger 是一个树形层级结构;
# Logger 可以包含一个或多个 Handler 和 Filter，
# 一个 Logger 实例可以新增多个 Handler，一个 Handler 可以新增多个 Formatter, Filter，
# 而且日志级别将会继承。

"""
logging模块使用过程
1, 第一次导入 logging 模块或使用 reload 函数重新导入 logging 模块，logging 模块中的代码
   将被执行，这个过程中将产生logging日志系统的默认配置。
2, 自定义配置(可选)。logging 标准模块支持三种配置方式: dictConfig，fileConfig，listen。
   其中，dictConfig 是通过一个字典进行配置 Logger，Handler，Filter，Formatter；
   fileConfig 则是通过一个文件进行配置；而 listen 则监听一个网络端口，通过接收网络数据
   来进行配置。当然，除了以上集体化配置外，也可以直接调用 Logger，Handler 等对象中的方法
   在代码中来显式配置。
3, 使用 logging 模块的全局作用域中的 getLogger 函数来得到一个 Logger 对象实例
   (其参数即是一个字符串，表示 Logger 对象实例的名字，即通过该名字来得到相应的 Logger
   对象实例)。
4, 使用 Logger 对象中的 debug，info，error，warn，critical 等方法记录日志信息。

logging 模块处理流程
1, 判断日志的等级是否大于 Logger 对象的等级，如果大于，则往下执行，否则，流程结束。
2, 产生日志。第一步，判断是否有异常，如果有，则添加异常信息。
   第二步，处理日志记录方法(如debug，info等)中的占位符，即一般的字符串格式化处理。
3, 使用注册到 Logger 对象中的 Filters 进行过滤。如果有多个过滤器，则依次过滤；
   只要有一个过滤器返回假，则过滤结束，且该日志信息将丢弃，不再处理，而处理流程也至此结束。
   否则，处理流程往下执行。
4, 在当前 Logger 对象中查找 Handlers，如果找不到任何 Handler，则往上到该 Logger 对象
   的父 Logger 中查找；如果找到一个或多个 Handler，则依次用 Handler 来处理日志信息。
   但在每个 Handler 处理日志信息过程中，会首先判断日志信息的等级是否大于该 Handler 的等级，
   如果大于，则往下执行(由 Logger 对象进入 Handler 对象中)，否则，处理流程结束。
5, 执行 Handler 对象中的 filter 方法，该方法会依次执行注册到该 Handler 对象中的 Filter。
   如果有一个 Filter 判断该日志信息为假，则此后的所有 Filter 都不再执行，而直接将该
   日志信息丢弃，处理流程结束。
6, 使用 Formatter 类格式化最终的输出结果。 注：Formatter 同上述第2步的字符串格式化不同，
   它会添加额外的信息，比如日志产生的时间，产生日志的源代码所在的源文件的路径等等。
7, 真正地输出日志信息(到网络，文件，终端，邮件等)。至于输出到哪个目的地，由 andler 的种类来决定。
"""


def main():
    pass


if __name__ == '__main__':
    main()
