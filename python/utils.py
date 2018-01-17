import re
import os
import codecs
import time
import operator
from functools import wraps


def timeit(fn):
    @wraps(fn)
    def timer(*args, **kwargs):
        ts = time.time()
        result = fn(*args, **kwargs)
        te = time.time()
        f = lambda arg : type(arg)
        print "\n************************************"
        print "function    = {0}".format(fn.__name__)
        print "  arguments = {0} {1}".format([f(arg) for arg in args], kwargs)
        # print "    return    = {0}".format(result)
        print "  time      = %.6f sec" % (te-ts)
        print "************************************\n"
        return result
    return timer

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

def readLice(filename, file_encoding, N):
    with codecs.open(filename, 'r', file_encoding) as inf:
        chunk = islice(inf, N)
        while chunk:
            yield chunk
            chunk = islice(inf, N)

def readChunk(filename, file_encoding, size):
    with codecs.open(filename, 'r', file_encoding) as inf:
        _header = inf.readline()
        chunk = inf.read(size)
        while chunk:
            yield chunk
            chunk = inf.read(size)


def readFilenames(corpus_path, fnames_ext, file_encoding):
    """
    this method does not accept leading or trailing whitespace in filenames
    """
    try:
        retVal = []
        fname = '{}.{}'.format(corpus_path, fnames_ext)
        with codecs.open(fname, 'r', file_encoding) as inFile:
            for curLine in inFile:
                curLine = curLine.strip()  # removes EOL, possibly more
                if len(curLine) > 0:
                    retVal.append(curLine)
    except IOError:
        retVal = [f for f in os.listdir(corpus_path)
                  if os.path.isfile(os.path.join(corpus_path, f)) and f not in {'.', '..'}]

    return retVal

def loadDictFromFile(filename, file_encoding='utf-8'):
    resDict = dict()
    with codecs.open(filename, 'r', file_encoding) as inFile:
        for line in inFile:
            pair = line.strip().split('\t')
            if len(pair) < 2:
                continue
            resDict[pair[0]] = float(pair[1]) if '.' in pair[1] else int(pair[1])
    return resDict

def saveDict2File(dict, filename, file_encoding='utf-8', order='alpha', freqCutOff=0):
    with codecs.open(filename, 'w', file_encoding) as outFile:
        if order == 'alpha':
            if isinstance(dict.keys()[0], str):
                for key, value in sorted(dict.iteritems(), key=operator.itemgetter(0)):
                    # the codecs.open() file.write() takes unicode string as parameter
                    # so the normal str should encode as file_encoding format
                    outFile.write('{}\t{}\n'.format(key, value).decode(file_encoding))
            else:
                for key, value in sorted(dict.iteritems(), key=operator.itemgetter(0)):
                    # but the line below for the case:
                    #   not convert unicode str of file to normal str
                    #   while dealing with corpus file
                    # here the key is unicode and the value is integer
                    outFile.write(u'{}\t{}\n'.format(key, value))
        elif order == 'freq':
            if isinstance(dict.keys()[0], str):
                for key, value in sorted(dict.iteritems(), key=operator.itemgetter(1), reverse=True):
                    outFile.write('{}\t{}\n'.format(key, value).decode(file_encoding))
            else:
                for key, value in sorted(dict.iteritems(), key=operator.itemgetter(1), reverse=True):
                    outFile.write(u'{}\t{}\n'.format(key, value))
        else:
            raise ValueError, "Error: unsupported order!"

def newSpan(size):
    retVal = []
    for i in range(size):
        retVal.append(None)
    return retVal


def newCoText(settings):
    """
    builds an object that keeps track of the current co-text
    Used by: addColFreq(filename, freqDict, settings)
    """
    retVal = {}
    retVal["node"] = None
    retVal["left-span"] = newSpan(settings["left-span"])
    retVal["right-span"] = newSpan(settings["right-span"])
    return retVal


def updateCoText(coText, line, settings):
    """
    FUNCTION: updates coText to the new line, represented by line
    MAKES USE OF: -
    USED BY:  makeTokenVectors()
    """
    if settings["left-span"] > 0:
        coText["left-span"].append(coText["node"])
        coText["left-span"] = coText["left-span"][1:]
    if settings["right-span"] > 0:
        coText["right-span"].append(line)
        coText["node"] = coText["right-span"][0]
        coText["right-span"] = coText["right-span"][1:]
    else:
        coText["node"] = line


def sumOfFDict(dict):
    retVal = 0
    for key in dict:
        retVal += dict[key]
    return retVal


def aTokRelFreq(num, denom):
    """
    adjusted relative token frequency
    actually, true relative frequency times 10000.0
    assumes denom > 0
    """
    return (num * 10000.0) / denom

def calcDirection(freq1, freq2):
    """
    :param freq1:
    :param freq2:
    :return:
    """
    return -1 if freq1 < freq2 else 1

def incDictFreq(dict, key, inc):
    if dict.has_key(key):
        dict[key] += inc
    else:
        dict[key] = inc
