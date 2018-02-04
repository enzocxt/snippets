# -*- coding: utf-8 -*-


'''
任何对象，只要正确实现了上下文管理，就可以用于with语句。
实现上下文管理是通过__enter__和__exit__这两个方法实现的，
也可以通过@contextmanager和closing函数实现
'''
import logging
import functools
import traceback

def trace(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        indent = ' ' * len(traceback.extract_stack())
        try:
            logging.debug('{0}entering {1}'.format(indent, fn.__name__))
            return fn(*args, **kwargs)
        except:
            logging.debug('{0}exception in {1}'.format(indent, fn.__name__))
            raise
        else:
            logging.debug('{0}leaving {1}'.format(indent, fn.__name__))

    return wrapper


def main():
    pass

if __name__ == '__main__':
    main()
