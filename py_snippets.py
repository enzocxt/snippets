# -*- coding: utf-8 -*-

from pathos.multiprocessing import Pool
import sys
sys.path.append("/home/enzocxt/Projects/QLVL/typetoken_workdir")
from collections import defaultdict
import math, re, codecs

# -------------------------------- ascii 码 ----------------------------------
'''
The Unicode standard describes how characters are represented by code points.
A code point is an integer value, usually denoted in base 16.
Encoding: the rules for translating a Unicode string into a sequence of bytes

Python’s default encoding is the ‘ascii’ encoding.
The rules for converting a Unicode string into the ASCII encoding are simple;
for each code point:
    1. If the code point is < 128, each byte is the same as the value of the
       code point.
    2. If the code point is 128 or greater, the Unicode string can’t be
       represented in this encoding.
       (Python raises a UnicodeEncodeError exception in this case.)

UTF-8 is one of the most commonly used encodings. UTF stands for “Unicode
Transformation Format”, and the ‘8’ means that 8-bit numbers are used in the
encoding.
(There’s also a UTF-16 encoding, but it’s less frequently used than UTF-8.)
UTF-8 uses the following rules:
    1. If the code point is <128, it’s represented by the corresponding byte
       value.
    2. If the code point is between 128 and 0x7ff, it’s turned into two byte
       values between 128 and 255.
    3. Code points >0x7ff are turned into three- or four-byte sequences,
       where each byte of the sequence is between 128 and 255.

Latin-1, also known as ISO-8859-1, is a similar encoding.
Unicode code points 0–255 are identical to the Latin-1 values,
so converting to this encoding simply requires converting code points to byte
values; if a code point larger than 255 is encountered, the string can’t be
encoded into Latin-1.

Unicode strings are expressed as instances of the unicode type, one of
Python’s repertoire of built-in types. It derives from an abstract type called
basestring, which is also an ancestor of the str type.

'''
def test_ascii():
    '''
    The unicode() constructor has the signature unicode(string[, encoding,
    errors]). All of its arguments should be 8-bit strings. The first argument
    is converted to Unicode using the specified encoding; if you leave off the
    encoding argument, the ASCII encoding is used for the conversion, so
    characters greater than 127 will be treated as errors:
    '''
    s = u'\u0234'.encode('utf8')    # encode 之后，s 是 str 类型
    print type(s)
    utf8 = [u'\u0123'.encode('utf8'), u'\u0234'.encode('utf8')]
    s = ''.join(utf8)   # 不会出错
    # s = u''.join(utf8)    # UnicodeEncodeError
    # 因为 utf8 中的元素是 str 类型
    # s = ''.join(utf8 + [u'unicode object'])   # UnicodeEncodeError
    # '' 是 str 类型，参数中由 unicode 类型
    l = '\t\t\t3.14\t\t'.split('\t')
    print len(l)
    print len(l[0])
    exit(-1)
    s = unicode('abcdef' + chr(255))
    # UnicodeDecodeError: 'ascii' codec can't decode byte 0xff in position 6:
    # ordinal not in range(128)
    '''
    One-character Unicode strings can also be created with the unichr()
    built-in function, which takes integers and returns a Unicode string of
    length 1 that contains the corresponding code point.
    The reverse operation is the built-in ord() function that takes a one-
    character Unicode string and returns the code point value:
    '''
    print unichr(40960)
    print ord(u'\ua000')

# 这里的 a 是 ascii 码字符串，无法直接转换成 string，如何解决？


# ------------------------------ python 多进程 --------------------------------
'''
'''
'''
虽然子进程复制了父进程的代码段和数据段等，但是一旦子进程开始运行，
子进程和父进程就是相互独立的，它们之间不再共享任何数据。
Python 提供了一个 multiprocessing 模块，利用它，我们可以来编写跨平台的多进程程序，
但需要注意的是 multiprocessing 在 Windows 和 Linux 平台的不一致性：
一样的代码在 Windows 和 Linux 下运行的结果可能不同。
因为 Windows 的进程模型和 Linux 不一样，Windows 下没有 fork。
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

# ----------------------------------------------------------------------------
import math
import os, sys, re
import time
import codecs
import operator
from itertools import islice
from collections import defaultdict
from tqdm import tqdm
import cPickle as pickle

from multiprocessing import Process, cpu_count
from multiprocessing.sharedctypes import Array
from pathos.multiprocessing import Pool
from multiprocessing.pool import ThreadPool
from threading import Thread
import Queue
#from concurrent.futures import ProcessPoolExecutor as Executor
from ctypes import c_char_p

from Dict import FrequencyDict, CollocDict
from utils import timeit, readFilenames, newCoText, updateCoText

import numpy as np


class Manager(object):

    def __init__(self, corpusName, settings):
        self.corpusName  = corpusName
        self.settings    = settings
        self.corpus_path = settings['corpus-path']
        self.output_path = settings['output-path']
        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)
        self.file_encoding = settings['file-encoding']

    def saveTypeID2File(self, filename):
        '''
        with open(filename, 'w') as outFile:
            for word, id in sorted(self.type2id.iteritems(), key=operator.itemgetter(1)):
                outFile.write(u'{}\t{}\n'.format(word, id).encode(self.settings['file-encoding']))
        '''
        pickle.dump(self.type2id, open(filename, 'wb'))

    def loadTypeIDFromFile(self, filename):
        '''
        with open(filename, 'r') as inFile:
            for line in inFile:
                word, id = line.strip().split('\t')
                self.type2id[word] = int(id)
        '''
        self.type2id = pickle.load(open(filename, 'rb'))
        return self.type2id

    def saveContextID2File(self, filename):
        '''
        with open(filename, 'w') as outFile:
            for word, id in sorted(self.type2id.iteritems(), key=operator.itemgetter(1)):
                outFile.write(u'{}\t{}\n'.format(word, id).encode(self.settings['file-encoding']))
        '''
        pickle.dump(self.context2id, open(filename, 'wb'))

    def loadContextIDFromFile(self, filename):
        '''
        with open(filename, 'r') as inFile:
            for line in inFile:
                word, id = line.strip().split('\t')
                self.type2id[word] = int(id)
        '''
        self.context2id = pickle.load(open(filename, 'rb'))
        return self.context2id

    @staticmethod
    def getLambda(attr):
        nums = map(int, attr.split(','))
        return lambda m: '/'.join(map(m.group, nums))


class ColFreqManager(Manager):

    def __init__(self, corpusName, settings, wordFile=None, contextFile=None):
        """
        :param wordFile: dict, defaultdict, or filename
        :param contextFile: dict, defaultdict, or filename
        """
        super(ColFreqManager, self).__init__(corpusName, settings)
        self.matrix = defaultdict(lambda: defaultdict(int))
        self.wordDict = CollocDict(freqDict=wordFile, file_encoding=self.file_encoding)
        self.contextDict = CollocDict(freqDict=contextFile, file_encoding=self.file_encoding)

    @timeit
    def makeColFreq(self, prog_bar=True):
        """
        The function will treat all different word types as possible target or context words
        and will record all co-occurrences in a file with one co-occurrencing pair per line
        in the format targetword + TAB + contextword + TAB + frequency.
        The output file has the extension '.colfreq'.
        :param wordFile:
        :param contextFile:
        :param freqCutoff:
        :return:
        """
        print("\nMaking col frequency matrix: {}".format(self.corpusName))
        file_encoding = self.settings['file-encoding']
        fnames_ext = self.settings['fnames-ext']
        corpus_path = self.corpus_path
        fnames = readFilenames(corpus_path, fnames_ext, file_encoding)
        fnames = ['{}/{}'.format(corpus_path, fn) for fn in fnames]
        if prog_bar:
            # pfnames = tqdm(fnames, unit='file', desc=corpus_path.split('/')[-1])
            pfnames = tqdm(fnames, unit='file', desc='  corpus')
        else:
            pfnames = fnames

        matrix = defaultdict(lambda: defaultdict(int))
        for fn in pfnames:
            self.addColFreq(matrix, fn, prog_bar=prog_bar)
        self.matrix = matrix

        return self.matrix

    @timeit
    def makeColFreq_multi(self, prog_bar=False):
        """
        multiprocess version of 'makeColFreq'
        :return:
        """
        print("\nMaking col frequency matrix: {}".format(self.corpusName))
        print("  multiprocess version: use {} CPU cores".format(cpu_count() - 2))
        file_encoding = self.settings['file-encoding']
        fnames_ext = self.settings['fnames-ext']
        corpus_path = self.corpus_path
        fnames = readFilenames(corpus_path, fnames_ext, file_encoding)
        fnames = ['{}/{}'.format(corpus_path, fn) for fn in fnames]

        # divide fnames into n groups, n+1 is the number of CPU cores
        num_cores = cpu_count() - 2
        num_fnames = len(fnames)
        # to improve: more meanly divided
        N = int(math.ceil(float(num_fnames) / num_cores))
        fn_group = []
        for i in range(num_cores):
            start = N * i
            end = N * (i+1) if num_fnames > N * (i+1) else num_fnames
            fn_group.append(fnames[start:end])

        starttime = time.time()
        print "start time: %s" % starttime
        # use process pool and get return results of target function
        def use_pool(num_cores, fn_group):
            pool = Pool(processes=num_cores)
            result = []
            for i in range(num_cores):
                args = (fn_group[i], )
                job = pool.apply_async(self.count_multi, args=args)
                result.append(job)
            pool.close()
            pool.join()
            result = [r.get() for r in result]
            return result

        def use_map(num_cores, fn_group):
            pool = Pool(processes=num_cores)
            result = pool.map(self.count_multi, fn_group)
            return result

        # clean tmp directory
        tmp_dir = self.settings['tmp-path']
        for f in os.listdir(tmp_dir):
            os.remove('{}/{}'.format(tmp_dir, f))

        mxs = use_map(num_cores, fn_group)
        print "processes finish: %s" % time.time()

        # merge matrices computed by all processes
        matrix = defaultdict(lambda: defaultdict(int))

        for mx in mxs:
            for rkey, row in mx.iteritems():
                for ckey, v in row.iteritems():
                    matrix[rkey][ckey] += v

        self.matrix = matrix
        print time.time()

        pid = os.getpid()
        filename = '{}/{}.tmp'.format(tmp_dir, pid)
        self.save2File(filename, matrix)
        return self.matrix

    @timeit
    def makeColFreq_multithr(self, prog_bar=False):
        """
        multiprocess version of 'makeColFreq'
        :return:
        """
        print("\nMaking col frequency matrix: {}".format(self.corpusName))
        print("  multiprocess version: use {} CPU cores".format(cpu_count() - 2))
        file_encoding = self.settings['file-encoding']
        fnames_ext = self.settings['fnames-ext']
        corpus_path = self.corpus_path
        fnames = readFilenames(corpus_path, fnames_ext, file_encoding)
        fnames = ['{}/{}'.format(corpus_path, fn) for fn in fnames]

        # divide fnames into n groups, n+1 is the number of CPU cores
        num_cores = cpu_count() - 2
        num_fnames = len(fnames)
        # to improve: more meanly divided
        N = int(math.ceil(float(num_fnames) / num_cores))
        fn_group = []
        for i in range(num_cores):
            start = N * i
            end = N * (i+1) if num_fnames > N * (i+1) else num_fnames
            fn_group.append(fnames[start:end])

        starttime = time.time()
        print "start time: %s" % starttime
        # use process pool and get return results of target function
        result = []
        queue = Queue.Queue()
        for i in range(num_cores):
            args = (fn_group[i], queue)
            job = Thread(target=self.count_multithr, args=args)
            job.daemon = True
            job.start()
            result.append(queue.get())

        print "threads finish: %s" % time.time()
        while not queue.empty():
            result.append(queue.get())
        # merge matrices computed by all processes
        matrix = defaultdict(lambda: defaultdict(int))
        mxs = result
        for mx in mxs:
            for rkey, row in mx.iteritems():
                for ckey, v in row.iteritems():
                    matrix[rkey][ckey] += v

        self.matrix = matrix
        return self.matrix

    def count_multithr(self, fnames, queue):
        matrix = defaultdict(lambda: defaultdict(int))
        for fn in fnames:
            self.addColFreq(matrix, fn, prog_bar=False)
        print time.time()
        queue.put(matrix)

    def count_multi(self, fnames):
        matrix = defaultdict(lambda: defaultdict(int))
        for fn in fnames:
            self.addColFreq(matrix, fn, prog_bar=False)
        print time.time()
        # return self.matrix2Arrays(matrix)
        tmp_dir = self.settings['tmp-path']
        pid = os.getpid()
        filename = '{}/{}.tmp'.format(tmp_dir, pid)
        self.save2File(filename, matrix)
        return matrix

    def save2File(self, filename, matrix):
        with codecs.open(filename, 'w', self.file_encoding) as outFile:
            for rkey, row in matrix.iteritems():
                for ckey, val in row.iteritems():
                    line = u'{}\t{}\t{}\n'.format(rkey, ckey, val)
                    outFile.write(line)
        print '{}: {}'.format(os.getpid(), time.time())

    def matrix2Arrays(self, matrix):
        rindex, cindex, values = [], [], []
        # matrix is a dict of dict
        for rkey in sorted(matrix.keys()):
            for ckey, val in matrix[rkey].iteritems():
                rindex.append(rkey)
                cindex.append(ckey)
                values.append(val)
        s = str('\t'.join(rindex))
        rindex = Array('c', s)
        #rindex = Array(c_char_p, rindex)
        #cindex = Array(c_char_p, cindex)
        #values = Array('i', values)
        #return rindex, cindex, values
        return rindex

    def addColFreq(self, matrix, filename, prog_bar=True):
        sett = self.settings
        coText = newCoText(sett)
        posLineMachine = sett['word-line-machine']
        sepLineMachine = sett['separator-line-machine']

        with codecs.open(filename, 'r', sett['file-encoding']) as inFile:
            if prog_bar:
                pdata = tqdm(inFile, desc='    {}'.format(filename.split('/')[-1]))
            else:
                pdata = inFile
            for curLine in pdata:
                curLine = curLine.strip()
                posmatch = posLineMachine.match(curLine)
                sepmatch = sepLineMachine.match(curLine)

                if posmatch:
                    updateCoText(coText, curLine, sett)
                    self.updateFreqDict(matrix, coText)
                elif sepmatch:
                    while coText['node']:
                        updateCoText(coText, None, sett)
                        self.updateFreqDict(matrix, coText)
                    coText = newCoText(sett)

        while coText["node"]:
            updateCoText(coText, None, sett)
            self.updateFreqDict(matrix, coText)

    def updateFreqDict(self, matrix, coText):
        sett = self.settings
        wDict, cDict = self.wordDict, self.contextDict
        if coText["node"] is None:
            return

        posLineMachine = sett['word-line-machine']
        nodeMatch = posLineMachine.match(coText['node'])
        get_node = self.getLambda(sett['get-node'])
        nodeString = get_node(nodeMatch)

        if (wDict.FILTERPRESENT and
            nodeString not in wDict):
            return

        for i in range(sett["left-span"]):
            if coText["left-span"][i] is None:
                continue
            match = posLineMachine.match(coText["left-span"][i])
            # colString = sett["get-colloc"](match)
            nums = map(int, sett['get-colloc'].split(','))
            get_colloc = lambda m: '/'.join(map(m.group, nums))
            colString = get_colloc(match)

            if (not cDict.FILTERPRESENT or
                colString in cDict):
                # self.contextDict[colString] += 1
                matrix[nodeString][colString] += 1

        for i in range(sett["right-span"]):
            if coText["right-span"][i] is None:
                continue
            match = posLineMachine.match(coText["right-span"][i])
            # colString = sett["get-colloc"](match)  # draws col from match
            nums = map(int, sett['get-colloc'].split(','))
            get_colloc = lambda m: '/'.join(map(m.group, nums))
            colString = get_colloc(match)

            if (not cDict.FILTERPRESENT or
                colString in cDict):
                # self.contextDict[colString] += 1
                matrix[nodeString][colString] += 1


# ----------------------------- python 文件操作 -------------------------------
# 删除文件和目录
import os
import shutil

def file_op():
    path = "/Users/enzo/Dropbox/CT/Luminocity/htdocs/img/books"
    dirs = os.listdir(path)     # 列出目录中所有文件或子目录
    for d in dirs:
        if d.startswith('.'):
            continue
        p = '{}/{}/original'.format(path, d)
        if os.path.isdir(p):    # os.path.exists(p) 文件是否存在
            shutil.rmtree(p)    # 删除目录及其所有文件
            # os.remove() 删除文件
            # os.rmdir() 删除空目录

# -------------------------------- 文件结束符 ----------------------------------
# 读到文件结尾时读到的不是 None，而是空字符''
def test_fileEnd():
    filename = '/home/enzocxt/Dropbox/CT/Useful/python_log.py'
    count = 0
    with open(filename, 'r') as inFile:
        line = inFile.readline()
        count += 1
        while True:
            if line is None or len(line) <= 0:
                # 如果去掉 len(line) <= 0 这个条件，会死循环
                break
            line = inFile.readline()
            count += 1
    print count

class Test(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def test_attr(self):
        a, b = self.__getattr__('a'), self.__getattr__('b')
        print a, b

# ----------------------------- main -----------------------------------------
from Config import ConfigLoader
if __name__ == '__main__':
    #corpus_path = "/home/enzocxt/Projects/QLVL/corp/en/BROWN_family/Brown_wpr-art"
    #ex = ProcessEx()
    #ex.makeItemFreq()

    default_conf = "/home/enzocxt/Projects/QLVL/typetoken_workdir/typetokenQLVL/config.ini"
    conf = ConfigLoader(default_conf)
    # update settings by user specified config file
    new_conf = "/home/enzocxt/Projects/QLVL/typetoken_workdir/test/config_test.ini"
    settings = conf.updateConfig(new_conf)
    # the better way for setting corpus directory, output directory, etc
    # is setting them in a configuration ini file in advance
    corpusName = 'Brown_wpr-art'
    corpus_path = settings['corpus-path']
    output_path = settings['output-path']

    # add temporary directory for temp files
    settings['tmp-path'] = "/home/enzocxt/Dropbox/CT/Useful/tmp"
    tmp_dir = settings['tmp-path']

    form = 'node'
    order = 'freq'

    wordFile = '{}/{}.NounsLowercase.minfreq10.nodefreq'.format(output_path, corpusName)
    contextFile = '{}/{}.minfreq10.without50mostfreq.nodefreq'.format(output_path, corpusName)

    #colfreq = ColFreqManager(corpusName, settings, wordFile=wordFile, contextFile=contextFile)
    # colfreq.makeColFreq()
    # colfreq.makeColFreq_multi()
    # colfreq.makeColFreq_multithr()

    test = Test('a', 'b')
    test.test_attr()
