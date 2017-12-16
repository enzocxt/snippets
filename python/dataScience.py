# -*- coding: utf-8 -*-

import sys, io
import codecs

from utils import timeit

import numpy as np
import pandas as pd


def test_ndarray_size():
    # NumPy数组需要占据连续的内存空间，即使内存足够但是内存中没有一块足够大的连续内存的话也是会出现MemoryError的。

    # 32位整型
    ai32 = np.array([], dtype=np.int32)
    bi32 = np.arange(1, dtype=np.int32)
    ci32 = np.arange(20, dtype=np.int32)

    # 64位整型
    ai64 = np.array([], dtype=np.int64)
    bi64 = np.arange(1, dtype=np.int64)
    ci64 = np.arange(20, dtype=np.int64)

    # 32位浮点数
    af32 = np.array([], dtype=np.float32)
    bf32 = np.arange(1, dtype=np.float32)
    cf32 = np.arange(100, dtype=np.float32)

    # 64位浮点数
    af64 = np.array([], dtype=np.float64)
    bf64 = np.arange(1, dtype=np.float64)
    cf64 = np.arange(100, dtype=np.float64)

    print(ci32.nbytes)      # 数组存储的值所占空间大小
    print(ci32.itemsize)    # 数组中每个值所占空间大小

    print("size of 0 int32 number: %s" % sys.getsizeof(ai32))
    print("size of 1 int32 number: %f" % sys.getsizeof(bi32))
    print("size of 20 int32 numbers: %f\n" % sys.getsizeof(ci32))

    print("size of 0 int64 number: %f" % sys.getsizeof(ai64))
    print("size of 1 int64 number: %f" % sys.getsizeof(bi64))
    print("size of 20 int64 numbers: %f\n" % sys.getsizeof(ci64))

    print("size of 0 float32 number: %f" % sys.getsizeof(af32))
    print("size of 1 float32 number: %f" % sys.getsizeof(bf32))
    print("size of 100 float32 numbers: %f\n" % sys.getsizeof(cf32))

    print("size of 0 float64 number: %f" % sys.getsizeof(af64))
    print("size of 1 float64 number: %f" % sys.getsizeof(bf64))
    print("size of 100 float64 numbers: %f" % sys.getsizeof(cf64))

'''
方法
1. block += inl， block 是 str 类型
   而每次 str 相加产生新的 block 时，因为 str 相加是复制后产生新的 str
   如果 str 长度很大，复制相加的开销很大
2. block.append(inl.strip())
   每一行作为 list 的元素，时间开销降低
'''
def readNLines(filename, file_encoding, N):
    with codecs.open(filename, 'r', file_encoding) as inf:
        i = 0
        headers = inf.readline()
        block = []
        for inl in inf:
            i += 1
            block.append(inl.strip())
            if i % N == 0:
                yield block
                block = []
        yield block

@timeit
def test_largefile(filename):
    N = 1000000
    nlines = 0
    blocks = readNLines(filename, 'latin1', N)
    i = 0
    for blk in blocks:
        # 1000000 行（100 MB）字符串转换成 list 之后所占空间大小是：
        print sys.getsizeof(blk)
        exit(-1)
        nlines += len(blk)
        i += 1
        print i,
        if i % 20 == 0:
            print '\n',
    print("lines of file: {}".format(nlines))

@timeit
def test_pd_large(filename):
    header = None
    with codecs.open(filename, 'r', 'latin1') as inf:
        i = 0
        header = inf.readline()
    header = header.strip().split('\t')

    N = 1000000
    blocks = readNLines(filename, 'latin1', N)
    headers = None
    for blk in blocks:
        data = u'\n'.join(blk)
        df = pd.read_csv(io.StringIO(data), names=header, sep='\t', na_values=['*'], error_bad_lines=False, low_memory=False)
        print df.columns
        print df.dtypes
        exit(-1)


if __name__ == '__main__':
    filename = "/home/enzocxt/Projects/QLVL/typetoken_workdir/tokenclouds/input/LeNC-4-4.1000000.colstats"
    test_pd_large(filename)
