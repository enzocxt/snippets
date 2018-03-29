# 使用 pyenv
# https://github.com/pyenv/pyenv
$ git clone https://github.com/pyenv/pyenv.git ~/.pyenv
# 后面的目录是 pyenv 的根目录，用户可以自己选择


# 安装 python
$ tar zxvf Python-2.7.13.tgz
$ cd Python-2.7.13
$ ./configure --prefix=/home/tao/.local
$ make
$ make install
# --prefix 指明 Python 安装在哪个目录下
# 安装好的 Python 命令就在 /home/tao/.local/bin/python

# 安装 virtualenv
$ tar zxvf virtualenv-15.1.0.tar.gz
$ cd virtualenv-15.1.0
$ /home/tao/.local/bin/python virtualenv.py PY_VENV
# /path/to/python virtualenv.py /path/to/venv/directory

# 如果当前文件系统缺少 symlinks 模块（无法使用类似命令 ln -s target link）
# 会出现 AttributeError: 'module' object has no attribute 'symlink' 错误
# 此时可以使用 --always-copy 参数
# /path/to/python virtualenv.py --always-copy /path/to/venv/directory

# 安装 pypy 的 virtual environment

# 下载 pypy 安装包并安装
$ tar xf pypy2-v5.9.0-linux64.tar.bz2
# 在 r2d2 上能使用， /path/to/pypy/bin/pypy --version
# 在 robin 上不能使用：
# ./bin/pypy: error while loading shared libraries: libssl.so.1.0.0:
# cannot open shared object file: No such file or directory

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

# PyPy 不能安装
# Failed cleaning build dir for scipy， scikit-learn
