# -*- coding: utf-8 -*-

import sys
import numpy as np
import pandas as pd

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

# NumPy数组需要占据连续的内存空间，即使内存足够但是内存中没有一块足够大的连续内存的话也是会出现MemoryError的。
