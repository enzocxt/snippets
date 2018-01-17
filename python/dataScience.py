# -*- coding: utf-8 -*-

import sys, io
import codecs
import time
import csv
from itertools import islice

from utils import timeit, readNLines, readLice, readChunk

import numpy as np
import pandas as pd


class npUtils(object):
    def __init__(self, filename=None):
        self.filename = filename

    def test_ndarray_size(self):
        # NumPy数组需要占据连续的内存空间，即使内存足够但是内存中没有一块足够大的
        # 连续内存的话也是会出现MemoryError
        # 内存块以按行（C 风格）或按列（FORTRAN 或 MatLab 风格）的方式保存元素。

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

    def npOperations(self):
        a = np.array([1,2,3])
        print a     # [1, 2, 3]
        a = np.array([[1,2], [3,4]])
        print a
        # [[1, 2]
        #  [3, 4]]
        # 最小维度
        a = np.array([1,2,3,4,5], ndmin=2)
        print a     # [[1, 2, 3, 4, 5]]
        # dtype 参数
        a = np.array([1,2,3], dtype=complex)
        print a     # [ 1.+0.j,  2.+0.j,  3.+0.j]

        # 创建结构化数据类型
        student = np.dtype([('name', 'S20'), ('age', 'i1'), ('marks', 'f4')])
        print student
        # [('name', 'S20'), ('age', 'i1'), ('marks', '<f4')])
        a = np.array([('abc',  21,  50),('xyz',  18,  75)], dtype = student)
        print a
        # [('abc', 21, 50.0), ('xyz', 18, 75.0)]

        # shape
        a = np.array([[1,2,3], [4,5,6]])
        print a.shape       # (2, 3)
        a.shape = (3, 2)
        print a             # [[1, 2] [3, 4] [5, 6]]
        # 也可以用 reshape 函数来调整数组大小
        a = np.array([[1,2,3], [4,5,6]])
        b = a.reshape(3, 2)
        print b             # [[1, 2] [3, 4] [5, 6]]
        print b.ndim        # 2

        # 等间隔数字的数组
        a = np.arange(10)
        print a             # [0 1 2 3 4 5 6 7 8 9]
        a = np.arange(24)
        b = a.reshape(2, 4, 3)
        print b             # b 现在是一个 3 维 数组


'''
方法
1. block += inl， block 是 str 类型
   而每次 str 相加产生新的 block 时，因为 str 相加是复制后产生新的 str
   如果 str 长度很大，复制相加的开销很大
2. block.append(inl.strip())
   每一行作为 list 的元素，时间开销降低
'''

class pdUtils(object):
    def __init__(self, filename=None):
        self.filename = filename

    @timeit
    def nlines(self, filename):
        fname = self.filename if self.filename else filename
        N = 1000000
        nlines = 0
        blocks = readNLines(fname, 'latin1', N)
        i = 0
        print "'.' represents for {} lines of file".format(N)
        for blk in blocks:
            nlines += len(blk)
            i += 1
            print '.',
            if i % 20 == 0:
                print '\n',
        print("\nlines of file: {}".format(nlines))
        return nlines

    @timeit
    def test_pd_large(self):
        starttime = time.time()

        tokens = ['wolk/noun', 'zon/noun', 'wolk_DIM/noun',
                  'zon_DIM/noun', 'wolkje/noun', 'zonetje/noun']

        with codecs.open(self.filename, 'r', 'latin1') as inf:
            i = 0
            header = inf.readline()
        header = header.strip().split('\t')
        # collocate, node, cur_c_a_b, cur_c_a_nb, cur_c_na_b, cur_c_na_nb
        # cur_lik_stat, cur_p_compl, wfreq_b, wfreq_nb, direction

        # N = 1000000
        # blocks = readNLines(filename, 'latin1', N)
        N = 100 * 1024 * 1024
        blocks = readChunk(filename, 'latin1', N)

        i = 0
        df_dtypes = {'collocate': unicode,
                         'node': unicode,
                         'cur_c_a_b': np.int64,
                         'cur_c_a_nb': np.int64,
                         'cur_c_na_b': np.int64,
                         'cur_c_na_nb': np.int64,
                         'cur_lik_stat': np.float64,
                         'cur_p_compl': np.float64,
                         'wfreq_b': np.float64,
                         'wfreq_nb': np.float64,
                         'direction': np.float64}
        lastLine = ''
        for blk in blocks:
            # data = u'\n'.join(blk)

            firstIdx = blk.find('\n')
            lastIdx = blk.rfind('\n')
            print '**** last line ****\n{}\n****************'.format(lastLine)
            data = lastLine + blk[:lastIdx]
            lastLine = blk[(lastIdx+1):]
            #data = blk[(firstIdx+1):lastIdx]
            #lastLine = lastLine + blk[:(firstIdx+1)] + blk[(lastIdx+1):]
            '''
            ERROR:
            pandas.errors.ParserError: Error tokenizing data.
            C error: EOF inside string starting at line
            The line listed with the 'EOF inside string' had a string
            that contained within it a single quote mark.
            add the option quoting=csv.QUOTE_NONE it fixed the problem
            '''
            df = pd.read_csv(io.StringIO(data), names=header, sep='\t', dtype=df_dtypes,
            error_bad_lines=False, quoting=csv.QUOTE_NONE, low_memory=False)

            print df.shape
            print df.dtypes
            # print df[df['node'].isin(tokens)][['collocate', 'node']]
            # print "---------------------------"
            # print df[df.node=="alone/name"][['collocate', 'node']]
            # print "{} lines processed".format(i * N)
            print "{} time cost".format(time.time() - starttime)
            # print "*******************************************"
            starttime = time.time()
            i += 1
            if i > 2:
                exit(-1)

    def test_encoding(self):
        notfound = {(u'Maleisi\xeb/name', u'zon/noun'),
                    (u'Itali\xeb/name', u'zon/noun'),
                    (u'Normandi\xeb/name', u'wolk/noun'),
                    (u'ori\xebntatie/noun', u'zon/noun'),
                    (u'Belgi\xeb/name', u'zon/noun'),
                    (u'zonnecr\xe8me/noun', u'zon/noun'),
                    (u'\xe0/vg', u'zon/noun'),
                    (u'ge\xefnspireerd/adj', u'zon/noun'),
                    (u'Californi\xeb/name', u'zon/noun')}
        notfound = {(u'Belgi\xeb/name', u'zon/noun')}
        df_dtypes = {'collocate': str,
                     'node': str,
                     'cur_c_a_b': np.int64,
                     'cur_c_a_nb': np.int64,
                     'cur_c_na_b': np.int64,
                     'cur_c_na_nb': np.int64,
                     'cur_lik_stat': np.float64,
                     'cur_p_compl': np.float64,
                     'wfreq_b': np.float64,
                     'wfreq_nb': np.float64,
                     'direction': np.float64}
        with codecs.open(self.filename, 'r', 'latin1') as inf:
            i = 0
            header = inf.readline().strip().split('\t')
            for inl in inf:
                inl = inl.strip()
                df = pd.read_csv(io.StringIO(inl),
                                 names=header, sep='\t', dtype=df_dtypes,
                                 quoting=csv.QUOTE_NONE, encoding='utf-8')
                coll_pd = df.loc[0, 'collocate']

                eles = inl.split('\t')
                if len(eles) < 2:
                    continue
                coll_f, node_f = eles[0], eles[1]

                if coll_f == unicode("$^©/num", 'utf-8'):
                    print coll_pd
                    print coll_f
                    exit(-1)
                if coll_pd != coll_f:
                    print coll_pd
                    print coll_pd.encode('utf-8')
                    print coll_f
                    exit(-1)
                i += 1
                if i % 1000000 == 0:
                    print i
                #key = (coll_f, node_f)
                '''
                if coll == u'Belgi\xeb/name':
                    print "last key {}".format(str(last))
                    print "found key {} on line {}".format(str(key), i)
                if key in notfound:
                    print "last key {}".format(str(last))
                    print "found key {} on line {}".format(str(key), i)
                '''


if __name__ == '__main__':
    # lines of this file: 70567602
    filename = "/home/enzocxt/Projects/QLVL/typetoken_workdir/tokenclouds/input/LeNC-4-4.colstats"
    # test_pd_large(filename)
    # test_encoding(filename)
    test = pdUtils()
    test.nlines(filename)
