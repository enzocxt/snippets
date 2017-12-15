import os
import time
import Queue

import numpy as np
import multiprocessing as mp
from multiprocessing import Process, Pool
from pathos.multiprocessing import Pool
from threading import Thread


# ------------------------------ python 多进程 --------------------------------

'''
进程创建的多个线程中产生的数据，是属于各线程私有的么？
这些线程产生的数据在进程中是否可以直接使用？是否需要复制一份到进程空间才能使用？
是否可以在进程中事先创建这些数据结构，而在线程中分别写入数据，而使得不用给线程加锁？
'''

'''
虽然子进程复制了父进程的代码段和数据段等，但是一旦子进程开始运行，
子进程和父进程就是相互独立的，它们之间不再共享任何数据。
Python 提供了一个 multiprocessing 模块，利用它，我们可以来编写跨平台的多进程程序，
但需要注意的是 multiprocessing 在 Windows 和 Linux 平台的不一致性：
一样的代码在 Windows 和 Linux 下运行的结果可能不同。
因为 Windows 的进程模型和 Linux 不一样，Windows 下没有 fork。
'''

'''https://stackoverflow.com/questions/26514172/returning-large-objects-from-child-processes-in-python-multiprocessing
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

# problem 1:
# 当同时执行单进程程序和多进程程序时，多进程程序的执行时间会变长很多
# 可能时因为内存中保存了单进程程序的结果，导致读取多进程程序返回值时时间增长

# problem 2:
# 矩阵运算 如何使用多线程

# 实验结果（robin server）：
# makeItemFreq_multi (7.8s) vs makeItemFreq (49s)
# makeColFreq_multi (68s) vs makeColFreq (83.4s)
# makeTCPosition_multi (5.4s) vs makeTCPosition (46.2s)

class ProcessEx(object):
    def __init__(self):
        self.freqDict = defaultdict(int)

    def makeItemFreq(self):
        data = ['a', 'c', 'b', 'd', 'b', 'c', 'd', 'b', 'a', 'd', 'c', 'b', 'a']
        num_cores = cpu_count() - 1
        num_eles = len(data)
        N = int (math.ceil(float(num_eles) / num_cores))
        data_group = []
        for i in range(num_cores):
            start = N * i
            end = N * (i + 1) if num_eles > N*(i+1) else num_eles
            data_group.append(data[start:end])

        # 使用Process数组的方式添加进程
        """
        ps = []
        for i in range(num_cores):
            ps.append(Process(target=self._count, args=(fnames_multi[i],)))
        for i in range(num_cores):
            ps[i].start()
        """

        # 使用进程池的方式
        # 使用 python 自带 multiprocessing
        # 不能使用类的方法（实例方法，类方法甚至静态方法）作为 target function
        # 因为它使用 pickle， 而 pickle fails to serialize the following
        #   Methods
        #   Lambdas
        #   Closures
        #   Some functions defined interactively
        # 所以要改用 pathos.multiprocessing
        # 创建进程池
        pool = Pool(processes=num_cores)
        result = []
        for i in range(num_cores):
            job = pool.apply_async(self.count, args=(data_group[i],))
            result.append(job)
        pool.close()    # 要先 close 进程池
        pool.join()

        dicts = [r.get() for r in result]
        freqDict = defaultdict(int)
        for d in dicts:
            for k, v in d.iteritems():
                freqDict[k] += v
        print freqDict

    def count(self, data):
        freqDict = defaultdict(int)
        for s in data:
            freqDict[s] += 1
        return freqDict


# -------------------------- Queues Communication ---------------------------
def writer(queue):
    pid = os.getpid()
    for i in range(1, 4):
        msg = i
        print "### writer {} -> {}".format(pid, msg)
        queue.put(msg)
        time.sleep(1)
        msg = 'Done'
    print '### writer {} -> {}'.format(pid, msg)
    queue.put(msg)

def reader(queue):
    pid = os.getpid()
    time.sleep(0.5)
    while True:
        msg = queue.get()
        print("--- reader {} -> {}".format(pid, msg))
        if msg == 'Done':
            break

def test_qcom():
    print("Initialize the experiment PID: {}".format(os.getpid()))
    manager = mp.Manager()
    queue = manager.Queue()

    pool = mp.Pool()
    pool.apply_async(writer, (queue,))
    pool.apply_async(reader, (queue,))

    pool.close()
    pool.join()

# ----------------- share numpy array between multiple processes ------------
def test_npshared():
    n = int(1e7)
    int_type = np.ctypeslib.ctypes.c_uint16
    # 以下时间均为 n = 1e7 时的情况
    # 68 ms: 创建了一个长度为 n 的数组，初始值为 0
    # <class '_ctypes.array.c_ushort_Array_10000000'>
    ct_arr1 = mp.RawArray(int_type, n)
    # 1.4 s: 从 python list 创建 ctypes 数组
    ct_arr2 = mp.RawArray(int_type, range(n))
    # 18.5 s: 从 numpy 数组创建 ctypes 数组
    #ct_arr2 = mp.RawArray(int_type, np.arange(n, dtype=np.uint16))
    # 2.4 s: 从 ctypes 数组拷贝一份到 ctypes 数组
    #ct_arr2 = mp.RawArray(int_type, ct_arr2)
    # 用 as_array() 从 ctypes 数组创建 numpy 数组， 非常快 2ms
    #np_arr = np.ctypeslib.as_array(ct_arr2)

    '''
    下面的第一种方法很慢的原因是：
    the (slow) RawArray slice assignment code,
    which in this case is inefficiently reading one raw C value at a time
    from the source array to create a Python object,
    then converts it straight back to raw C for storage in the shared array,
    then discards the temporary Python object, and repeats n times

    but, like most C level things, RawArray implements the buffer protocol,
    which means you can convert it to a memoryview,
    using raw memory operations if possible

    之后的工作： 尝试用 memoryview 和 Python 的 array 包 ！！！
    '''
    # 12.6 s: 将 numpy 数组复制给 ctypes 数组
    ct_arr1[:] = np.arange(n, dtype=np.uint16)
    # 424 ms: 使用 memoryview 来 assign memory
    memoryview(ct_arr1)[:] = np.arange(n, dtype=np.uint16)

    for i in xrange(n):
        # type(ct_arr1[i]) : <type 'int'>
        # 转换到了 python 内置类型？
        assert ct_arr1[i] == ct_arr2[i]



if __name__ == '__main__':
    # test_qcom()
    test_npshared()
