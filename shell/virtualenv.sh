# 安装 pypy 的 virtual environment

# 下载 pypy 安装包并安装
$ tar xf pypy2-v5.9.0-linux64.tar.bz2
$ mv pypy2-v5.9.0-linux64 /home/enzocxt/.local/lib/pypy2
# 建立软链接
$ ln -s /home/enzocxt/.local/lib/pypy2/bin/pypy /home/enzocxt/.local/bin/pypy

# 创建 virtual environment: http://doc.pypy.org/en/latest/install.html
$ virtualenv -p /home/enzocxt/.local/bin/pypy /home/enzocxt/Projects/Pypy_VIRTUALENV
$ source /home/enzocxt/Process/Pypy_VIRTUALENV/bin/activate
# 之后， 在 Pypy_VIRTUALENV 中，python 是指向 pypy 的一个软链接， 可以直接使用
(Pypy_VIRTUALENV) $ python --version
Python 2.7.13 (84a2f3e6a7f8, Oct 03 2017, 11:00:55)
[PyPy 5.9.0 with GCC 6.2.0 20160901]
