# -*- coding: utf-8 -*-

import os
import sys
import codecs
import locale


'''
ASCII 码： 127 个字符
中国制定了 GB2312 编码，日本有 Shift_JIS，...
各国有各国的标准，无法避免冲突。多语言混合文本中，会有乱码。
Unicode 应运而生。它将所有语言都统一到一套编码里。
常用的 Unicode 用两个字节表示一个字符（如果用到偏僻字符，则要4个字节）

ASCII编码和Unicode编码的区别：ASCII编码是1个字节，而Unicode编码通常是2个字节。
字母 A 用 ASCII 编码是十进制的 65，二进制的 01000001；
汉字“中”已经超出了 ASCII 编码的范围，用 Unicode 编码是十进制的 20013，
二进制的01001110 00101101。
你可以猜测，如果把 ASCII 编码的 A 用 Unicode 编码，只需要在前面补0就可以，
因此，A 的 Unicode编码是 00000000 01000001。

但是虽然乱码问题没有了，
如果所需字符基本都是英文，用 Unicode 编码比 ASCII 编码需要多一倍的空间
进而又出现了把 Unicode 编码转化为“可变长编码”的 UTF-8 编码

字符	ASCII	   Unicode	            UTF-8
A	 01000001	00000000 01000001	 01000001
中	x	        01001110 00101101	 11100100 10111000 10101101

因为 Python 的诞生比 Unicode 标准发布的时间还要早，所以最早的 Python 只支持 ASCII 编码，
普通的字符串'ABC'在 Python 内部都是 ASCII 编码的。
Python 提供了 ord() 和 chr() 函数，可以把字母和对应的数字相互转换：

Python2 中默认编码方式是 ASCII，Python3 是 UTF-8
Python2 中使用 a='中文' 定义的字符串其实不是真正的字符串，它不是 Unicode，所以说在定义 a 时
默认进行了一次编码转换，这个编码转换和上面的 ASCII 还没有关系，使用的是另一种默认的编码
这两种默认编码在 Python3 中几乎不会用到，它们产生的原因在于 Python2 设计上的缺陷

1. 定义 str 时的自动编码
在 Python2 中，a = '中文'这个 a 不是 Unicode，b = u'中文'这个 b 才是。
而在 Python3 中根本没有 u'中文' 这一说，a = '中文'这个 a 就是 Unicode。

准确地说，a 叫字节串，b 才叫字符串（前面提到过 Unicode 和字符串完全等同）。
a 其实是一个二进制字节流，是字符串 encode 后的产物。所以说在 a = '中文'这个赋值过程中，
默认进行了一次编码 encode，将’中文’这个字符串编码成了二进制数。
'''
def show1():
    dencoding = locale.getdefaultlocale()
    print(dencoding)


'''
2. str 和 Unicode 混用造成的错误
由于第一条中的差异，a = '中文'这样定义的 a 在编码和解码方面也与 Python3 是有不同的。

在python3中，这样定义的a只能encode，因为它是Unicode
在python2中，这个a主要是要decode，因为它是编码过的
从这一点中，第一种默认编码上场了。

如果 str 和 Unicode 混用，如 '中文' + u'好'，这个过程会将 str 解码成 Unicode，
使用的是默认编码方式（ASCII），而中文不对应 ASCII 编码，于是报错。

而在 Python3 中，如果 str 和 bytes 直接相加，会直接报出一个错误
TypeError: Can't convert 'bytes' object to str implicitly
Python3 说的很明确不能隐式转，而不是像 Python2 一样偷偷给你转了。
'''
def show2():
    # Python2 的默认编码是 ASCII，Python3 是 UTF-8
    df_encoding = sys.getdefaultencoding()
    print(df_encoding)
    s = '中文' + u'好'
    print(s)    # UnicodeDecodeError: 要将 '中文' decode 解码成 Unicode 字符串


'''
3. Python2 编码解码通用不规范造成的错误
1) Python3 中 str 和 bytes 分别对应 Python2 中的 Unicode 和 str
   Python2 中 a = '中文' 是 str 类，b = u'中文' 是 Unicode 类
2) Python2 中，无论 Unicode 类还是 str 类，都可以使用 encode 和 decode 方法，
   Python3 中明确 str 只能使用 encode，bytes 只能使用 decode


'''
def show3():
    '''
    UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-1: ordinal not in range(128)
    对 Unicode 强行 decode 报错，
    因为 Unicode 本身不能 decode，所以 Python2 默认将 Unicode 用 ASCII encode，
    再用得到的结果去 decode，而在 encode 的过程中就报错了
    '''
    a = '中文'
    a.encode('UTF-8')

    '''
    UnicodeDecodeError: 'ascii' codec can't decode byte 0xe4 in position 0: ordinal not in range(128)
    因为 str 本身不能 encode，Python2 默认将 str 用 ASCII decode，
    再用得到的结果 encode，所以在 decode 的过程中就报错了
    '''
    b = u'中文'
    b.decode('UTF-8')


'''
4. print() 时的默认编码
我们之前提到过，a = '中文' 这样定义的 a 其实本身是字节串而不是字符串，
在控制台中输入 a 的输出结果和输入 print(a) 的输出结果是不一样的
    输入a的输出结果是16进制形式的，也就是它的本来面貌
    输入print(a)的输出结果是我们能看懂的字符’中文’
说明
'''
def show4():
    '''
    在 print 时其实进行了一次默认解码，将字节转换成了 unicode 呈现出来。
    这时 print 的是 str 类型，如果传入的是 unicode 类型，又会自动按照 ascii 编码
    将 unicode encode 为 str，然后再 print 出来，如下所示
    (这个问题在最新 Python2.7 中不存在！！！)
    '''
    b = '中文'
    print(b)


'''
5. 函数参数类型传递错误
如果函数参数类型是 str，而传入的是 Unicode 类型时，会使用 ASCII 编码 encode
可以看成是 情况4 的推广，str 和 raw_input 函数都是这样
'''
def show5():
    b = u'中文'
    print(b)    # 这里不会出错
    str(b)
    a = raw_input(b)


def show():
    A = ord('A')
    _65 = chr(65)
    print(A)
    print(_65)

    zhong = u'中'
    print(zhong)

    c1 = u'ABC'.encode('utf-8')
    c2 = u'中文'.encode('utf-8')
    print(c1)
    print(type(c2))
    print(len(c2))



if __name__ == '__main__':
    # show()
    show4()
