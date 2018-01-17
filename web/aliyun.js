/**
？？？购买 ECS 服务器时，网络类型中的经典网络和专有网络有什么区别
？？？如果一个域名解析设置中添加了不同 IP 地址的服务器，该域名将会如何解析
 */

/**
有关购买 ECS 服务器和域名之后的绑定和解析流程
http://help.clouddream.net/newsitem/277595075

要将域名和服务器绑定，需要在域名解析设置中添加 A 记录
例如：
记录类型  主机记录  解析线路  记录值           TTL值  ...
A        www     默认      47.97.173.65    10分钟
 */


/** 添加安全组，开放 TCP 80 端口
购买好实例之后，阿里云的安全组中默认没有开放 HTTP 的 80 端口
需要用户添加安全组后才能访问
查看端口占用情况
$ lsof -i:80
 */


/** ssh 登录
实例 ID：i-wz9auskg5pl2ssika93s
公网 IP：120.79.156.87
远程连接密码：226343

首次使用 ssh 远程登录可以使用密码登录方式，
root 用户密码为 Aliyun007
登录之后可将客户端公钥信息写入服务器端 /root/.ssh/authorized_keys 文件中
参考：
https://help.aliyun.com/knowledge_detail/41493.html?spm=5176.7841468.2.9.bfw6Zi

1,
添加新用户：(# 是 root 用户的命令行提示符)
# adduser tao (密码是 1121007)
把用户添加到 sudo 组
# usermod -aG sudo tao
使用 su 命令切换到新用户
# su - tao
命令行提示符变成 $

2,
在用户目录添加目录 .ssh，拷贝公钥
# cp /root/.ssh/authorized_keys /home/tao/.ssh/authorized_keys
# su - tao
更改文件所属
$ sudo chown tao:tao /home/tao/.ssh/authorized_keys
（tao:tao 用户和用户组）
更改权限
$ sudo chmod 644 authorized_keys

3,
本地执行命令生成 id_rsa 和 id_rsa.pub，回车忽略密码
$ ssh-keygen -t rsa
如果要让多个服务（如 Github）对应多个秘钥：
生成 github 使用的秘钥：id_rsa.github
$ ssh-keygen -t rsa -C "enzocxt@gmail.com" -f id_rsa.github
[no passphrase]
额外将新生成的秘钥添加到环境中，切换到 .ssh 目录操作
$ ssh-add id_rsa.github
如果提示 "Could not open a connection to your authentication agent"
可以执行如下命令
$ ssh-agent bash
再执行 ssh-add 命令可以看到 "Identity added: id_rsa.github (id_rsa.github)"
查询已生成秘钥
$ ssh-add -l

4,
创建好密钥后到.ssh目录下创建一个 config 文件，配置参考：
# github
Host github.com
    HostName github.com
    PreferredAuthentications publickey
    IdentityFile /home/tao/.ssh/id_rsa.github
可以添加多个配置，如果服务器是 IP 直接在 Host 及 HostName 填写 IP 地址
该方法也可以给服务器用来设置别名
# Aliyun
Host aliyun
    HostName 47.97.173.65
    User tao
设置好之后就可以使用命令 $ ssh aliyun 来登录该 IP 指向的服务器了

5,
修改 SSH 的配置文件了
/etc/ssh/sshd_config
# 修改4个属性并去掉#号。
RSAAuthentication yes
PubkeyAuthentication yes
AuthorizedKeysFile %h/.ssh/authorized_keys
-----------------------------------------------------------------
使用 Putty Filezilla 登软件 SFTP 协议并使用账号密码登录时出现如下错误：
Disconnected:No supported authentication methods available
这是因为 ssh 的默认配置禁用了使用账号密码登录
修改文件 /etc/ssh/sshd_config （有时可能也要修改 /etc/ssh/ssh_config）
PasswordAuthentication yes
-----------------------------------------------------------------

6,
重启ssh服务
$ sudo service ssh restart

7,（可选）
如果普通用户能够使用 ssh 登录到服务器，则可以禁用 root 用户登录
/etc/ssh/sshd_config
PermitRootLogin no
 */


/** 安装 Nginx
安装 Nginx
$ sudo apt-get update
$ sudo apt-get install nginx

安装 MySQL
$ sudo apt-get install mysql-server
MySQL ROOT 管理用户密码 1121007

安装 php7.0
$ sudo apt-get -y install php7.0-fpm php-mysql
php-fpm 是一个 PHP FastCGI 管理器，是 PHP 源码的一个补丁
旨在将 FastCGI 进程管理整合进 PHP 中
新版 PHP 已经集成 php-fpm
 */


/**
在阿里云 ECS 服务器上安装 vsftpd 搭建 FTP 服务器
# apt-get install vsftpd

测试是否安装成功
# service vsftpd start
如果失败，首先检查 FTP 端口 20,21 是否被占用
# netstat -natp | grep 20, netstat -natp | grep 21

配置 vsftpd
文件结构：（Ubuntu）
1，/etc/vsftpd.conf 配置文件 （其它系统或安装情况可能会在 /etc/vsftpd/vsftpd.conf）
2，/etc/ftpusers （/etc/vsftpd/ftpusers）
ftpusers 里面装着本地用户列表，它的限制最大，是一个黑名单。凡是在用户列表中的用户，FTP账号是
不能使用。比如：root用户,如果ftpusers含有一个root用户且前面没有加#号。即表示FTP账号中禁止
使用root登录，即黑名单。因此如果你想要使用root账号来进行FTP登录，则需要在ftpusers文件中的
root前面加上#号，表示允许root用户作为FTP账号来登录。一般建议创建一个新的账号作为FTP账号。
3，/etc/user_list 或 /etc/vsftpd/user_list （没有这两个文件）

为FTP服务器添加指定账号
1.假设我的网站根目录 /var/www/html，并且我想用 webFTP 作为账号，password 作为密码。
2.使用命令添加账号以及赋予权限。
命令为：useradd webFTP -d /var/www/html -g ftp -s /sbin/nologin
-d 表示目录，必须为相对的根路径；
-g 指定分组 ftp;
-s 指定该用户不能反悔上一级；
命令：passwd webFTP（设置FTP账号密码）
3.给 /var/www/html 目录赋值 ftp 用户组权限权限。
命令为：chmod 773 /var/www/html

Filezilla 连接时出现 530 Login incorrect 错误
编辑文件 /etc/pam.d/vsftpd
注释禁用一下内容
#auth required pam_shells.so
 */

/**
---------------------------------- error -------------------------------------
??? sudo: unable to resolve host iZwz9auskg5pl2ssika93sZ
在 /etc/hosts 中添加一行：127.0.0.1 iZwz9auskg5pl2ssika93sZ
https://askubuntu.com/questions/59458/error-message-sudo-unable-to-resolve-host-user

配置文件中打开了匿名访问（anonymous=YES)
# vsftpd
500 OOPS: bad bool value in config file for: allow_writeable_chroot
注释这行变量之后
# vsftpd
500 OOPS: run two copies of vsftpd for IPv4 and IPv6
500 OOPS: could not bind listening IPv4 socket
500 OOPS: vsftpd: not configured for standalone, must be started from inetd
 */
