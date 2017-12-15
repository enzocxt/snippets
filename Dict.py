import re
import sys
import operator
from collections import defaultdict

import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt

from utils import loadDictFromFile, saveDict2File


class FrequencyDict(object):

    def __init__(self, freqDict=None, file_encoding='utf-8'):
        """
        :param freqDict:
            it could be a python dict or collections.defaultdict
            or it could be the filename of such a frequency dict
        :param file_encoding:
            encoding of corpus files, with default utf-8
        """
        self.freqDict = defaultdict(int)
        self.FILTERPRESENT = False
        self.file_encoding = file_encoding
        self.freqDict, self.FILTERPRESENT = self._construct(freqDict, file_encoding)

    @staticmethod
    def _construct(freqDict, file_encoding):
        if freqDict is None:
            return defaultdict(int), False
        elif isinstance(freqDict, defaultdict) or isinstance(freqDict, dict):
            # if the given freqDict is already a dict
            return freqDict, True
        elif isinstance(freqDict, str):
            # if the given freqDict is the filename of frequency dict
            return loadDictFromFile(filename=freqDict, file_encoding=file_encoding), True
        else:
            raise ValueError, "Error: the freqDict parameter should be a dict or dict filename!"

    # ------- basic methods -------
    def keys(self):
        return self.freqDict.keys()

    def values(self):
        return self.freqDict.values()

    def items(self):
        return self.freqDict.items()

    def iteritems(self):
        return self.freqDict.iteritems()

    def getFreqDict(self):
        return self.freqDict

    def getKeys(self):
        return self.freqDict.keys()

    def isEmpty(self):
        return True if not self.freqDict else False

    def setFILTER(self, value):
        self.FILTERPRESENT = value

    def __contains__(self, item):
        return item in self.freqDict

    def __getitem__(self, item):
        return self.freqDict[item]

    def __setitem__(self, key, value):
        self.freqDict[key] = value

    def __len__(self):
        return len(self.freqDict.keys())

    def increment(self, key, inc):
        if key in self.freqDict:
            self.freqDict[key] += inc
        else:
            self.freqDict[key] = inc

    # ------- file methods -------
    def saveDict2File(self, filename, order='alpha'):
        saveDict2File(self.freqDict, filename, self.file_encoding, order=order)

    @classmethod
    def load_dict(cls, filename, file_encoding='utf-8'):
        return loadDictFromFile(filename, file_encoding=file_encoding)

    def loadDictFromFile(self, filename, i=1, n='all', setToZero=False):
        """
        transform word/type/token frequency file to dictionary
        :param filename: frequency file name
        :param i:
        :param n:
        :param setToZero:
        :return:
        """
        self.freqDict = loadDictFromFile(filename, file_encoding=self.file_encoding)
        return self.freqDict

    def sumFreq(self):
        retVal = 0
        for key in self.freqDict:
            retVal += self.freqDict[key]
        return retVal

    # ------- filter methods -------
    def removeHigh(self, dict=None, threshold=0, num=0):
        """
        remove items:
            whose frequency is higher than threshold
            or whose frequency is among the 'num' highest
        :param dict: user could provide a dict, if not use the self.freqDict
        :param threshold: remove items whose frequency is higher than threshold
        :param num: remove the highest 'num' items
        :return: FrequencyDict object
        """
        if dict is None:
            dict = self.freqDict
        if threshold != 0:
            if num != 0:
                raise ValueError, "Could not use threshold and num at the same time!!!"
            else:
                ret = self.removeFreqHigherThan(dict, threshold)
        else:
            if num != 0:
                ret = self.removeHighest(dict, num)
            else:
                ret = self
        return ret

    @staticmethod
    def removeFreqHigherThan(dict=None, threshold=0):
        d = {k: v for k, v in dict.iteritems() if v <= threshold}
        return FrequencyDict(d)

    @staticmethod
    def removeHighest(dict=None, num=0):
        d = sorted(dict.iteritems(), key=operator.itemgetter(1), reverse=True)[num:]
        d = {k: v for k, v in d}
        return FrequencyDict(d)

    def removeLow(self, dict=None, threshold=0, num=0):
        """
        remove items:
            whose frequency is lower than threshold
            or whose frequency is among the 'num' lowest
        :param dict: user could provide a dict, if not use the self.freqDict
        :param threshold: remove items whose frequency is lower than threshold
        :param num: remove the lowest 'num' items
        :return: FrequencyDict object
        """
        if dict is None:
            dict = self.freqDict
        if threshold != 0:
            if num != 0:
                raise ValueError, "Could not use threshold and num at the same time!!!"
            else:
                ret = self.removeFreqLowerThan(dict, threshold)
        else:
            if num != 0:
                ret = self.removeLowest(dict, num)
            else:
                ret = self
        return ret

    @staticmethod
    def removeFreqLowerThan(dict=None, threshold=0):
        d = {k: v for k, v in dict.iteritems() if v >= threshold}
        return FrequencyDict(d)

    @staticmethod
    def removeLowest(dict=None, num=0):
        d = sorted(dict.iteritems(), key=operator.itemgetter(1), reverse=True)[:-num]
        d = {k: v for k, v in d}
        return FrequencyDict(d)

    def getNouns(self, dict=None):
        if dict is None:
            dict = self.freqDict
        # case 'xx//' would be a problem
        f = lambda x : True if len(x.split('/')[-1])>0 and x.split('/')[-1][0].lower() == 'n' else False
        d = {k: v for k, v in dict.iteritems() if f(k)}
        return FrequencyDict(d)

    def getVerbs(self, dict=None):
        if dict is None:
            dict = self.freqDict
        f = lambda x : x.split('/')[-1][0].lower() == 'v'
        d = {k: v for k, v in dict.iteritems() if f(k)}
        return FrequencyDict(d)

    def keepAlpha(self, dict=None):
        if dict is None:
            dict = self.freqDict
        f = lambda x : x.split('/')[0].isalpha()
        d = {k: v for k, v in dict.iteritems() if f(k)}
        return FrequencyDict(d)

    def keepLowercase(self, dict=None):
        if dict is None:
            dict = self.freqDict
        f = lambda x : x.split('/')[0].islower()
        d = {k: v for k, v in dict.iteritems() if f(k)}
        return FrequencyDict(d)

    def keepLengthLongerThan(self, dict=None, length=0):
        if dict is None:
            dict = self.freqDict
        f = lambda x : len(x.split('/')[0]) > length
        d = {k: v for k, v in dict.iteritems() if f(k)}
        return FrequencyDict(d)

    def getMostFreq(self, dict=None, num=0):
        """
        get a number of most frequent items
        :param num: return how many most frequent items
        :return: the filtered dict
        """
        if dict is None:
            dict = self.freqDict
        d = sorted(dict.iteritems(), key=operator.itemgetter(1), reverse=True)
        return FrequencyDict(dict(d[:num]))

    def getMostNonFreq(self, dict=None, num=0):
        """
        get a number of most non-frequent items
        :param num: return how many most non-frequent items
        :return: the filtered dict
        """
        if dict is None:
            dict = self.freqDict
        d = sorted(dict.iteritems(), key=operator.itemgetter(1))
        return FrequencyDict(dict(d[:num]))

    def filter_by_tagset(self, filename):
        tagset = set()
        with open(filename, 'r') as inFile:
            for line in inFile:
                tagset.add(line.strip().split('\t')[0])

        newDict = dict()
        for key, value in self.freqDict.iteritems():
            if key.split('/')[-1] in tagset:
                newDict[key] = value
        return FrequencyDict(newDict)

    def filter(self, regex=None, thresholdHigh=sys.maxint, numHighest=0, thresholdLow=0, numLowest=0, outFilename=None):
        """
        :param regex: give regular expression
        :param cutOff: cut off frequency
        :param numMostFreq: remove a number of most frequent items
        :param outFilename:
        :return:
        """

        items = sorted(self.freqDict.iteritems(), key=operator.itemgetter(1), reverse=True)
        # remove numHighest and numLowest items
        items = items[numHighest:(len(items) - numLowest)]
        # remove items with frequency larger than thresholdHigh and smaller than thresholdLow
        d = {k: v for k, v in items if thresholdLow <= v <= thresholdHigh}
        resDict = FrequencyDict(d)

        if not regex:
            return resDict

        # if user provides regular expression
        m = re.compile(regex)
        fdict = filter(lambda x: m.match(x[0]), d.items())
        fdict = dict(fdict)
        resDict = FrequencyDict(fdict)

        if outFilename:
            resDict.saveDict2File(outFilename)
        return resDict

    def some(self):
        # fig, ax = plt.subplots()
        data = sorted(self.freqDict.values())
        s = pd.Series(data)
        #s = s.value_counts()
        #s.plot(ax=ax)
        s.hist()
        # plt.show()


    def __repr__(self):
        items = self.freqDict.items()
        if len(items) <= 7:
            return '[{}]'.format(','.join(map(str, items)))
        items = sorted(items, key=operator.itemgetter(1), reverse=True)
        return '[{} ... {}]'.format(','.join(map(str, items[:3])),
                                    ','.join(map(str, items[-3:])))

    def __str__(self):
        return self.__repr__()


class CollocDict(FrequencyDict):
    """
    This CollocDict could be used for word dict and context dict.
    It has two attributes: freqDict and item2id
    freqDict: inherited freqDict of FrequencyDict
    item2id:  item to id mapping built on freqDict
    """
    def __init__(self, freqDict=None, file_encoding='utf-8', order='alpha'):
        """
        :param freqDict: dict or filename
            if freqDict is not None
            build item2id mapping
        """
        super(CollocDict, self).__init__(freqDict=freqDict, file_encoding=file_encoding)
        # if dict is not None, the super() function will build freqDict first
        self.item2id = defaultdict(int) if freqDict is None else self.buildItem2IDFromFreqDict(order=order)
        self._order = order

    def buildItem2IDFromFreqDict(self, dict=None, order='alpha'):
        """
        build item2id mapping from the frequency dict
        :param dict: frequency dict
        :param order: sort keys of dict based on the order
        :return: item2id mapping
        """
        # if not given dict parameter, use self.freqDict
        freqDict = dict if dict else self.freqDict
        # if freqDict is None or len(freqDict) == 0:
        if freqDict is None:
            raise ValueError, "Error: frequency dict is None!"

        if order == 'alpha':
            l = sorted(freqDict.keys())
        elif order == 'freq':
            tmp = sorted(freqDict.iteritems(), key=operator.itemgetter(1))
            l = [k for (k, _) in tmp]
        else:
            raise ValueError, "Unsupported sorting format!"

        self.item2id = defaultdict(int, {k: v for v, k in enumerate(l)})
        return self.item2id

    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, order):
        self._order = order

    def reorder(self, order):
        """
        Currently unused
        TODO: improve
        :param order: new order
        :return:
        """
        if order == self._order:
            print "No need to re-order!"
            return
        self.buildItem2IDFromFreqDict(order)
        self._order = order
