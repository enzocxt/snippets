# 查看用户所在的组
$ groups
users qlvl-corp semmetrix termwise ido sociolectormetry corpread mars aardvark
$ groups tao
tao: users qlvl-corp semmetrix termwise ido sociolectormetry corpread mars aardvark

# /etc/group 文件包含所有组
# /etc/group 的内容包括用户组（Group）、用户组口令、GID及该用户组所包含的用户（User），
# 每个用户组一条记录；格式如下：
# group_name:passwd:GID:user_list
#
# 在/etc/group 中的每条记录分四个字段：
# 第一字段：用户组名称；
# 第二字段：用户组密码；
# 第三字段：GID
# 第四字段：用户列表，每个用户之间用,号分割；本字段可以为空；如果字段为空表示用户组为GID的用户名；
$ less /etc/group
root:x:0:root
users:x:100:kris,...,heidi,tao,mariana
aardvark:x:516:dirk,kris,...,heidi,tao,mariana

# 创建用户组
groupadd users
# 添加用户到用户组
gpasswd -a tao users
# 为用户组删除用户
gpasswd -d tao users

# 添加新用户：(# 是 root 用户的命令行提示符)
adduser tao (密码是 1121007)
# 把用户添加到 sudo 组
usermod -aG sudo tao
# 使用 su 命令切换到新用户
su - tao
# 命令行提示符变成 $
# 删除用户user2
userdel user2
# 删除用户 user3，同时删除他的工作目录
userdel –r user3

# 更改文件所属
$ sudo chown tao:tao /home/tao/.ssh/authorized_keys
（tao:tao 用户和用户组）
# 更改权限
$ sudo chmod 644 authorized_keys
