import logging

# 教程：
# http://www.jianshu.com/p/feb86c06c4f4
# http://python.jobbole.com/81666/
# 几个比较重要的概念： Logger, Handler, Formatter, Filter
# Logger 记录器， 保留了应用程序代码能直接使用的借口
# Handler 处理器， 将（记录器产生的）日志记录发送至合适的目的地
# Filter 过滤器，提供了更好的粒度控制，它可以决定输出哪些日志记录
# Formatter 格式化器，指明了最终输出中日志记录的布局

logger = logging.getLogger('test')
logger.setLevel(logging.ERROR)      # 设置日志级别为 ERROR， 即只有日志级别大于等于 ERROR 的日志才会输出
logger.addHandler(handler_name)     # 为 Logger 实例增加一个处理器
logger.removeHandler(handler_name)  # 为 Logger 实例删除一个处理器
