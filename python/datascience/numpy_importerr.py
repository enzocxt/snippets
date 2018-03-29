# -*- coding: utf-8 -*-

""" for recording
(PY_VENV) enzocxt@Ubuntu-KUL:~/Projects/QLVL/typetoken_workdir/typetokenQLVL$ python snippets.py
Traceback (most recent call last):
  File "snippets.py", line 6, in <module>
    from typetoken.Manager import ItemFreqManager, ColFreqManager, MatrixManager, TokVecManager
  File "/home/enzocxt/Projects/QLVL/typetoken_workdir/typetokenQLVL/typetoken/Manager.py", line 16, in <module>
    import numpy as np
  File "/home/enzocxt/Projects/VENV/PY_VENV/lib/python2.7/site-packages/numpy/__init__.py", line 142, in <module>
    from . import add_newdocs
  File "/home/enzocxt/Projects/VENV/PY_VENV/lib/python2.7/site-packages/numpy/add_newdocs.py", line 13, in <module>
    from numpy.lib import add_newdoc
  File "/home/enzocxt/Projects/VENV/PY_VENV/lib/python2.7/site-packages/numpy/lib/__init__.py", line 8, in <module>
    from .type_check import *
  File "/home/enzocxt/Projects/VENV/PY_VENV/lib/python2.7/site-packages/numpy/lib/type_check.py", line 11, in <module>
    import numpy.core.numeric as _nx
  File "/home/enzocxt/Projects/VENV/PY_VENV/lib/python2.7/site-packages/numpy/core/__init__.py", line 74, in <module>
    from numpy.testing import _numpy_tester
  File "/home/enzocxt/Projects/VENV/PY_VENV/lib/python2.7/site-packages/numpy/testing/__init__.py", line 10, in <module>
    from unittest import TestCase
  File "/home/enzocxt/Projects/QLVL/typetoken_workdir/typetokenQLVL/unittest.py", line 6, in <module>
    from scipy import sparse
  File "/home/enzocxt/Projects/VENV/PY_VENV/lib/python2.7/site-packages/scipy/__init__.py", line 71, in <module>
    from numpy.random import rand, randn
  File "/home/enzocxt/Projects/VENV/PY_VENV/lib/python2.7/site-packages/numpy/random/__init__.py", line 99, in <module>
    from .mtrand import *
  File "numpy.pxd", line 87, in init mtrand
AttributeError: 'module' object has no attribute 'dtype'

原因：
snippets.py 文件的同目录内有一个 unittest.py 文件
而 `from unittest import TestCase` 这句是 numpy 自我测试时用的
目录内的 unittest.py 文件与 numpy 自带的测试文件同名
所以出错
将 unittest.py 文件移到别的目录之后，此错误解决！！！
"""
