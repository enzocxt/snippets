/** 基本信息
Public IP: 35.177.247.45
Public DNS: ec2-35-177-247-45.eu-west-2.compute.amazonaws.com
Instance ID: i-04878b9f4421cb3fd
 */

/**
要将域名绑定到 AWS，
去 GoDaddy 账户的 DNS Management 中添加 A 记录
 */

/** ssh 登录
第一次只能用 ubuntu 用户登录
登录之后重置 root 密码
ubuntu@ip-172-31-8-240:/$ cd root/
-bash: cd: root/: Permission denied
ubuntu@ip-172-31-8-240:/$ sudo passwd root
Enter new UNIX password:
Retype new UNIX password:
passwd: password updated successfully

ubuntu@ip-172-31-8-240:/$ su
Password:
root@ip-172-31-8-240:/#
成功切换到 root 用户

ssh 配置参考阿里云
 */

/** 安装 Nginx MySQL PHP 参考阿里云
MySQL ROOT 管理用户密码 1121007
 */
