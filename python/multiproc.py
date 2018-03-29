# -*- coding: utf-8 -*-

import os
import time
import Queue
import random

# import multiprocessing as mp
from multiprocessing import Process, Pool
# from pathos.multiprocessing import Pool
from threading import Thread


# ------------------------------ python 多进程 --------------------------------
''' Questions
进程创建的多个线程中产生的数据，是属于各线程私有的么？
这些线程产生的数据在进程中是否可以直接使用？是否需要复制一份到进程空间才能使用？
是否可以在进程中事先创建这些数据结构，而在线程中分别写入数据，而使得不用给线程加锁？

problem 1:
当同时执行单进程程序和多进程程序时，多进程程序的执行时间会变长很多
可能时因为内存中保存了单进程程序的结果，导致读取多进程程序返回值时时间增长

problem 2:
矩阵运算 如何使用多线程

虽然子进程复制了父进程的代码段和数据段等，但是一旦子进程开始运行，
子进程和父进程就是相互独立的，它们之间不再共享任何数据。
Python 提供了一个 multiprocessing 模块，利用它，我们可以来编写跨平台的多进程程序，
但需要注意的是 multiprocessing 在 Windows 和 Linux 平台的不一致性：
一样的代码在 Windows 和 Linux 下运行的结果可能不同。
因为 Windows 的进程模型和 Linux 不一样，Windows 下没有 fork。

https://stackoverflow.com/questions/26514172/returning-large-objects-from-child-processes-in-python-multiprocessing
如果返回值在子进程中创建，则必须通过 pickle 的方式传回给父进程
通过 Pipe 传输 pickled bytes 给父进程，然后在父进程 unpickle the object
For a large object, this is pretty slow in CPython, so it's not just a PyPy issue.

In CPython, there is a way to allocate ctypes objects in shared memory,
via multiprocessing.sharedctypes.

There is also multiprocessing.Manager,
which would allow you to create a shared array/list object in a Manager process,
and then both the parent and child could access the shared list via a Proxy object.
The downside there is that read/write performance to the object is much slower
than it would be as a local object, or even if it was a roughly equivalent object
created using multiprocessing.sharedctypes.
'''

def run_proc(name):
    print "Run child process {} ({})...".format(name, os.getpid())


def show_single_process():
    print "Parent process {}.".format(os.getpid())
    p = Process(target=run_proc, args=('test',))
    print "Process will start..."
    p.start()
    p.join()
    print "Process end."


def long_time_task(name):
    print "Run task {} ({})...".format(name, os.getpid())
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print "Task {} runs {:.2f} seconds.".format(name, (end - start))


def show_multi_tasks():
    print "Parent process {}.".format(os.getpid())
    p = Pool()
    for i in range(5):
        p.apply_async(long_time_task, args=(i,))
    print "Waiting for all subprocesses done..."
    p.close()
    p.join()
    print "All subprocesses done."


if __name__ == '__main__':
    show_multi_tasks()
