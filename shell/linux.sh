# ×××××××××××× Unix 文件系统的历史 ××××××××××××
在最初开发 Unix 系统时，由于操作系统（根目录）变得越来越大，
一块盘已经装不下，加上了第二块盘，并规定第一块盘专门放系统程序，
第二块盘专门放用户自己的程序，因此挂载的目录点取名为 /usr
也就是说，根目录 “/” 挂载在第一块盘，“/usr” 目录挂载在第二快盘
除此之外，两块盘的目录结构完全相同，第一块盘的目录（/bin, /sbin/, /lib, /tmp...）
都在 /usr 目录下重现一次
后来第二块盘也满了，只好又加了第三块盘，挂载的目录点取名为 /home，
并规定 /usr 用于存放用户的程序，/home 用于存放用户的数据
这种目录结构就延续了下来。
/: 存放系统程序，也就是 At&t 开发的 Unix 程序
/usr： 存放 Unix 系统商（比如 IBM 和 HP）开发的程序
/usr/local: 存放用户自己安装的程序
/opt： 在某些系统，用于存放第三方厂商开发的程序

# Python 安装目录
# 系统自带
/usr/bin/python2.7
/usr/bin/python2.7-config
/usr/lib/python2.7
/usr/include/python2.7
/usr/share/python

# 如果使用源码包安装 Python 到指定文件夹内（如 ~/.local/python2）
---- python2
    |---- bin
    |---- include
         |---- python2.7 (里面是所有的 .h 头文件)
    |---- lib
         |---- libpython2.7.a
         |---- pkgconfig
         |---- python2.7 (自带的库和第三方的库)
              |---- site-packages (第三方的库： numpy ...)
              |---- unittest
              |---- multiprocessing
              ...
    |---- share
         |---- man

There are three types of modules in Python.
1, pure Python modules - modules contained in a single .py file
2, extension modules - modules written in low-level languages like C
                       and have extensions such as .so, .pyd
3, packages - a directory in file system having a special file __init__.py
              (that makes it recognizable as a package by Python interpreter)
              containing Python modules or packages

# 文件组织
如何组织目录 $HOME/.local ???
组织成 /usr 目录一样：
.local: bin include lib share


Python build error
#×××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××
if test ! -d /home/aardvark/tools/.local/python2/lib/pkgconfig; then \
		echo "Creating directory /home/aardvark/tools/.local/python2/lib/pkgconfig"; \
		/usr/bin/install -c -d -m 755 /home/aardvark/tools/.local/python2/lib/pkgconfig; \
	fi
if test -f /home/aardvark/tools/.local/python2/bin/python -o -h /home/aardvark/tools/.local/python2/bin/python; \
	then rm -f /home/aardvark/tools/.local/python2/bin/python; \
	else true; \
	fi
(cd /home/aardvark/tools/.local/python2/bin; ln -s python2 python)
ln: failed to create symbolic link `python`: Operation not supported
make: *** [bininstall] Error 1
#×××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××

#×××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××
(PY_VENV) tao@r2d2:/home/aardvark/tools/VENV/PY_VENV$ pip install tqdm
Collecting tqdm
  Using cached tqdm-4.19.6-py2.py3-none-any.whl
Installing collected packages: tqdm
Exception:
Traceback (most recent call last):
  File "/home/aardvark/tools/VENV/PY_VENV/lib/python2.7/site-packages/pip/basecommand.py", line 215, in main
    status = self.run(options, args)
  File "/home/aardvark/tools/VENV/PY_VENV/lib/python2.7/site-packages/pip/commands/install.py", line 342, in run
    prefix=options.prefix_path,
  File "/home/aardvark/tools/VENV/PY_VENV/lib/python2.7/site-packages/pip/req/req_set.py", line 784, in install
    **kwargs
  File "/home/aardvark/tools/VENV/PY_VENV/lib/python2.7/site-packages/pip/req/req_install.py", line 851, in install
    self.move_wheel_files(self.source_dir, root=root, prefix=prefix)
  File "/home/aardvark/tools/VENV/PY_VENV/lib/python2.7/site-packages/pip/req/req_install.py", line 1064, in move_wheel_files
    isolated=self.isolated,
  File "/home/aardvark/tools/VENV/PY_VENV/lib/python2.7/site-packages/pip/wheel.py", line 345, in move_wheel_files
    clobber(source, lib_dir, True)
  File "/home/aardvark/tools/VENV/PY_VENV/lib/python2.7/site-packages/pip/wheel.py", line 329, in clobber
    os.utime(destfile, (st.st_atime, st.st_mtime))
OSError: [Errno 1] Operation not permitted: '/home/aardvark/tools/VENV/PY_VENV/lib/python2.7/site-packages/tqdm-4.19.6.dist-info/metadata.json'
#×××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××

#×××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××
Traceback (most recent call last):]
  File "/home/aardvark/tools/.local/python2/lib/python2.7/threading.py", line 801, in __bootstrap_inner
    self.run()
  File "/home/aardvark/tools/VENV/PY_VENV/lib/python2.7/site-packages/tqdm/_tqdm.py", line 148, in run
    for instance in self.tqdm_cls._instances:
  File "/home/aardvark/tools/VENV/PY_VENV/lib/python2.7/_weakrefset.py", line 60, in __iter__
    for itemref in self.data:
RuntimeError: Set changed size during iteration
--------------------------------------------------------------------------
you change the size of the set you are currently iterating over. You can avoid this by using
  for color in self.domains[var].copy():
Using copy() will allow you to iterate over a copy of the set, while removing items from the original.
#×××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××××
