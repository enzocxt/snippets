# ----------------------------- ssh ----------------------------------------

# log in rem80ofL1note server
$ ssh tao@robin.arts.kuleuven.be
# password: T80ofL1n

# 可能会出现无法将该远程地址加入到 ssh 的 hosts 中，检查 known_hosts 文件的权限
# 解决：
$ chmod 0600 ~/.ssh/known_hosts

# ssh 可以直接用命令 exit 退出

# 远程复制文件
# 在本地电脑运行
$ scp your_username@remotehost:/some/remote/directory/ /some/local/directorys

# ----------------------------- git ---------------------------------------
# git add 命令错误添加了某文件，如果想在 commit 前 undo 对该文件的 add
# You can undo git add before commit with
$ git reset <file>

# -------------------------------------------------------------------------
# 系统后台执行命令， 执行命令后可以继续使用终端
$ python snippets.py &

# ----------------------------- 进程性能分析 --------------------------------
# top 命令是 linux 下常用的性能分析工具， 能够实时显示系统中各个进程的资源占用情况
# 可以直接使用 top 命令后，查看 %MEM 的内容
# 可以选择按进程查看或者按用户查看
$ top -u tao

# 按数字键 1，可以查看每个 cpu 的使用情况

# PID（进程ID）, USER（进程所有者）, PR（进程的优先级别，越小越优先被执行）,
# NI（Ninice值）, VIRT（进程占用的虚拟内存）, RES（进程占用的物理内存）,
# SHR（进程使用的共享内存）, S（进程状态： S uspend，R unning, Z ombie, N egative,
# %CPU（进程占用CPU的使用率）, %MEM（进程使用的物理内存和总内存的百分比）,
# TIME+（该进程启动后占用的总 CPU 时间， 即占用 CPU 使用时间的累加值, COMMAND（进程启动命令）
# 常用命令：
# P：按 %CPU 使用率排行
# T：按 TIME+ 排行
# M：按 %MEM 排行

# 可以根据进程查看进程相关信息占用内存的情况，进程号可以通过 ps 查看
$ pmap -d 14596

# 总核数 = 物理 CPU 个数 X 每颗物理 CPU 的核数
# 总逻辑 CPU 数 = 物理 CPU 个数 X 每颗物理 CPU 的核数 X 超线程数 ？？？
# 查看物理 CPU 个数
$ cat /proc/cpuinfo | grep "physical id" | sort -u
physical id   : 0
# 查看每个物理 CPU 中 core 的个数（即核数）
$ cat /proc/cpuinfo | grep "cpu cores" | uniq
cpu cores     : 2
# 查看逻辑 CPU 的个数
$ cat /proc/cpuinfo | grep "processor" | wc -l
4
# 4/2=2, 可见该 CPU 支持并已打开超线程

# ----------------------------- 链接 ----------------------------------------
$ ln -s source_file dest_file
# 软链接： -s 建立的是软链接
# 1.软链接，以路径的形式存在。类似于Windows操作系统中的快捷方式
# 2.软链接可以 跨文件系统 ，硬链接不可以
# 3.软链接可以对一个不存在的文件名进行链接
# 4.软链接可以对目录进行链接
# 硬链接:
# 1.硬链接，以文件副本的形式存在。但不占用实际空间。
# 2.不允许给目录创建硬链接
# 3.硬链接只有在同一个文件系统中才能创建
