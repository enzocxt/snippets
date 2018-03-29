import re
import sys
import operator
from collections import defaultdict

import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt


class FrequencyDict(object):

    def __init__(self, freq_dict=None, file_encoding='utf-8'):
        """
        :param freq_dict:
            it could be a python dict or collections.defaultdict
            or it could be the filename of such a frequency dict
        :param file_encoding:
            encoding of corpus files, with default utf-8
        """
        self.freq_dict = defaultdict(int)
        self.FILTERPRESENT = False
        self.file_encoding = file_encoding
        self.freq_dict, self.FILTERPRESENT = self._construct(freq_dict, file_encoding)

    @staticmethod
    def _construct(freq_dict, file_encoding):
        if freq_dict is None:
            return defaultdict(int), False
        elif isinstance(freq_dict, defaultdict) or isinstance(freq_dict, dict):
            # if the given freq_dict is already a dict
            return freq_dict, True
        elif isinstance(freq_dict, str):
            # if the given freq_dict is the filename of frequency dict
            return loadDictFromFile(filename=freq_dict, file_encoding=file_encoding), True
        else:
            raise ValueError, "Error: the freq_dict parameter should be a dict or dict filename!"

    def __contains__(self, item):
        return item in self.freq_dict

    def __getitem__(self, item):
        if isinstance(item, list):
            d = dict()
            if len(item) > 0:
                if isinstance(item[0], str):
                    return self._select_by_items(item)
                elif isinstance(item[0], int):
                    return self._select_by_freqs(item)
                else:
                    raise NotImplementedError
            else:
                return FrequencyDict(d)
        elif isinstance(item, tuple):
            d = self
            for i in range(len(item)):
                cond = item[i]
                d = d.__getitem__(cond)
            return d
        elif isinstance(item, str):
            return self.freq_dict[item]
        else:
            raise NotImplementedError

    def _select_by_items(self, items):
        d = dict()
        items_set = set(items)
        for k, v in self.freq_dict.iteritems():
            if k in items_set:
                d[k] = v
        return FrequencyDict(d)

    def _select_by_freqs(self, freqs):
        d = dict()
        freqs_set = set(freqs)
        for k, v in self.freq_dict.iteritems():
            if v in freqs_set:
                d[k] = v
        return FrequencyDict(d)

    def __setitem__(self, key, value):
        self.freq_dict[key] = value

    def __getattr__(self, attr):
        if attr == 'freq':
            return self

    def __lt__(self, other):
        res = []
        if isinstance(other, int):
            for k, v in self.freq_dict.iteritems():
                if v < other:
                    res.append(k)
        else:
            raise NotImplementedError

        return res

    def __le__(self, other):
        res = []
        if isinstance(other, int):
            for k, v in self.freq_dict.iteritems():
                if v <= other:
                    res.append(k)
        else:
            raise ValueError("Error: unsupported value!")

        return res

    def __eq__(self, other):
        res = []
        if isinstance(other, int):
            for k, v in self.freq_dict.iteritems():
                if v == other:
                    res.append(k)

    def __gt__(self, other):
        res = []
        if isinstance(other, int):
            for k, v in self.freq_dict.iteritems():
                if v > other:
                    res.append(k)
        else:
            raise ValueError("Error: unsupported value!")

        return res

    def __ge__(self, other):
        res = []
        if isinstance(other, int):
            for k, v in self.freq_dict.iteritems():
                if v >= other:
                    res.append(k)
        else:
            raise ValueError("Error: unsupported value!")

        return res

    def __len__(self):
        return len(self.freq_dict.keys())

    # ------- basic methods -------
    def keys(self):
        return self.freq_dict.keys()

    def values(self):
        return self.freq_dict.values()

    def items(self):
        return self.freq_dict.items()

    def iteritems(self):
        return self.freq_dict.iteritems()

    def get_dict(self):
        return self.freq_dict

    def isEmpty(self):
        return True if not self.freq_dict else False

    def setFILTER(self, value):
        self.FILTERPRESENT = value

    def __repr__(self):
        items = self.freq_dict.items()
        if len(items) <= 7:
            return '[{}]'.format(','.join(map(str, items)))
        items = sorted(items, key=operator.itemgetter(1), reverse=True)
        return '[{} ... {}]'.format(','.join(map(str, items[:3])),
                                    ','.join(map(str, items[-3:])))

    def __str__(self):
        return self.__repr__()


if __name__ == '__main__':
    d = {'a': 1,
         'b': 2,
         'c': 3,
         'd': 4,
         'e': 5,}
    freq_dict = FrequencyDict(freq_dict=d)
    print(freq_dict[2 < freq_dict.freq, freq_dict.freq < 4.4])
