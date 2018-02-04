# -*- coding: utf-8 -*-


# 使用 argparse 处理命令行参数
# Python 标准库中有关处理命令行的方案： getopt, optparse, argparse
def show_argparse():
    import argparse
    parse = argparse.ArgumentParser()
    parse.add_argument('-o', '--output')
    parse.add_argument('-v', dest='verbose', action='store_true')
    args = parser.parse_args()


# 一般情况下使用 ElementTree 解析 XML
# 给一个较好的学习教程： http://pycoders-weekly-chinese.readthedocs.io/en/latest/issue6/processing-xml-in-python-with-element-tree.html
def show_elementtree():
    try:
        import xml.etree.cElementTree as ET
    except ImportError:
        import xml.etree.ElementTree as ET

    count = 0
    for event, elem in ET.iterparse('test.xml'):
        if event == 'end':
            if elem.tag == 'userid':
                count += 1
        elem.clear()
    print(count)


# 使用 traceback 获取栈信息
# Python程序的traceback信息均来源于一个叫做traceback object的对象，
# 而这个traceback object通常是通过函数sys.exc_info()来获取的
def show_traceback():
    import sys
    import traceback

    exc_type, exc_value, exc_traceback_obj = sys.exc_info()
    # traceback.print_tb(tb[, limit[, file]])
    # traceback.print_tb(exc_traceback_obj)
    # traceback.print_exception(etype, value, tb[, limit[, file]])
    traceback.print_exception(exc_type, exc_value, exc_traceback_obj, limit=2, file=sys.stdout)
    # print_exc 是简化版的 print_exception
    # traceback.print_exc([limit[, file]])
    traceback.print_exc(limit=2, file=sys.stdout)
    # 想通过 logger 将异常记录在 log 里，这个时候就需要 format_exc 了，
    # 它跟 print_exc 用法相同，只是不直接打印而是返回了字符串
    logger.error(traceback.format_exc(limit=1, file=sys.stdout))
    # 从当前栈中提取 trace 信息
    traceback.extract_stack([file, [, limit]])


def main():
    show_elementtree()


if __name__ == '__main__':
    main()
