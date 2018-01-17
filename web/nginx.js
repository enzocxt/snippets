/** install
# root 用户直接安装
apt-get install nginx

使用源码安装
如果使用源码安装 ./configure 时可能会出现 pcre（一个正则表达式库）库的依赖错误
$ sudo apt-get install libpcre3 libpcre3-dev 安装之后问题解决
解压源码之后使用 --prefix 参数提供安装路径
$ ./configure --prefix=/home/enzocxt/.local/nginx
--------------------------------------------------------------------------
Configuration summary
  + using system PCRE library
  + OpenSSL library is not used
  + using system zlib library

  nginx path prefix: "/home/enzocxt/.local/nginx"
  nginx binary file: "/home/enzocxt/.local/nginx/sbin/nginx"
  nginx modules path: "/home/enzocxt/.local/nginx/modules"
  nginx configuration prefix: "/home/enzocxt/.local/nginx/conf"
  nginx configuration file: "/home/enzocxt/.local/nginx/conf/nginx.conf"
  nginx pid file: "/home/enzocxt/.local/nginx/logs/nginx.pid"
  nginx error log file: "/home/enzocxt/.local/nginx/logs/error.log"
  nginx http access log file: "/home/enzocxt/.local/nginx/logs/access.log"
  nginx http client request body temporary files: "client_body_temp"
  nginx http proxy temporary files: "proxy_temp"
  nginx http fastcgi temporary files: "fastcgi_temp"
  nginx http uwsgi temporary files: "uwsgi_temp"
  nginx http scgi temporary files: "scgi_temp"
--------------------------------------------------------------------------
$ make && make install
$ ln -s /home/enzocxt/.local/nginx/sbin/nginx /home/enzocxt/.local/bin/nginx
查看是否安装成功
$ nginx -v
 */

/** 介绍
Nginx 由一个主线程（master process）和几个工作线程（worker process）
主线程的目的时加载和验证配置文件、维护工作线程
工作线程处理实际的请求，Nginx 采用基于事件的模型和依赖操作系统的机制在工作线程之间高效地分发请求。
工作线程的数量可配置，也可自动调整为服务器CPU的数量。
Nginx 及其模块的工作方式由配置文件确定。 默认情况下，配置文件名为 nginx.conf，
放在 /usr/local/nginx/conf 、/etc/nginx 或者 /usr/local/etc/nginx 文件夹中。
 */

/** 基本命令
$ nginx -s <signal>
其中 -s 意思是向主进程发送信号，signal 可以为以下四个中的一个:
stop — 快速关闭
quit — 优雅关闭
reload — 重新加载配置文件
reopen — 重新打开日志文件
当运行 nginx -s quit 时，Nginx 会等待工作进程处理完成当前请求，然后将其关闭。
当你修改配置文件后，并不会立即生效，而是等待重启或者收到 nginx -s reload 信号。
当 Nginx 收到 nginx -s reload 信号后，首先检查配置文件的语法。
语法正确后，主线程会开启新的工作线程并向旧的工作线程发送关闭信号，
如果语法不正确，则主线程回滚变化并继续使用旧的配置。
当工作进程收到主进程的关闭信号后，会在处理完当前请求之后退出。
 */

/** 文件结构
文件结构：
conf（存放 nginx 相关的配置文件，最核心的时 nginx.conf）
html（默认的网站根目录）
logs（日志文件目录，访问日志，错误日志，运行时的PID）
sbin（主程序 nginx 目录）

Ubuntu apt-get 安装后的默认文件结构：
1，所有的配置文件都在 /etc/nginx 下，并且每个虚拟主机已经安排在了/etc/nginx/sites-available下
2，程序文件在 /usr/sbin/nginx
3，日志放在了 /var/log/nginx中
4，并已经在 /etc/init.d/ 下创建了启动脚本 nginx
5，默认的虚拟主机的目录设置在了 /var/www/nginx-default (有的版本 默认的虚拟主机的目录设置在了/var/www, 请参考/etc/nginx/sites-available里的配置)

当 Nginx 进程运行时，PID 号默认存放在 /prefix/nginx/logs/nginx.pid 或 /run/nginx.pid 文件中
因此若改用 kill 命令，也可以根据 nginx.pid 文件中的 PID 号来进行控制
# killall -9 nginx
 */

/** 配置： https://lufficc.com/blog/nginx-for-beginners
Nginx 配置的核心是定义要处理的 URL 以及如何响应这些 URL 请求，
即定义一系列的虚拟服务器（Virtual Servers）控制对来自特定域名或者 IP 的请求的处理。

每一个虚拟服务器定义一系列的 location 控制处理特定的 URI 集合。
每一个location定义了对映射到自己的请求的处理场景，可以返回一个文件或者代理此请求。

复制默认设置文件 default 来创建一份配置给新的网站
$ cd /etc/nginx/sites-available/
$ cp default demoooi.cc

建立个软连接到 sites-enabled，因为在配置文件 nginx.conf 中使用了 sites-enabled
$ ln -s /etc/nginx/sites-available/demoooi.com /etc/nginx/sites-enabled/demoooi.cc

修改新站点配置:
listen 80 default_server;
改成:
listen 80; //注意:default_server是设置默认站点的,我们新建立的站点不需要

root /var/www/html
改成:
root /web/www/demoooi  (写你自己的网站目录)

server_name _;
改成：
server_name demoooi.cc www.demoooi.cc;
（加上 www.demoooi.cc 保证访问带 www 的网址时也能使用该配置）

重启nginx服务:
sudo nginx -s reload
 */

/** Errors
$ nginx
初次运行会出现如下错误
nginx: [emerg] bind() to 0.0.0.0:80 failed (13: Permission denied)
这是因为 conf 文件中默认的端口号是 80
而 linux 下 socket 要绑定 1024 以下的端口号时需要 root 权限
在 conf 文件中将 http -> server 中的 listen 端口号 改为任意大于 1024 的就可以了 (8888)
再在浏览器中查看 localhost:8888 可以看到 Nginx 的欢迎页面

配置文件 nginx.conf 主要分为六个区域：
main（全局设置）、events（ nginx 工作模式）
http（ http 设置）： server（主机设置）、location（ URL 匹配）、upstream（负载均衡服务器设置）
？？？
配置文件中只有 http 设置，具体 server location 等保存在 sites-available/default 文件中

如果出现 80 端口被占用的情况
http://blog.csdn.net/ownfire/article/details/7966645
如果出现 error: unable to resolve host iZbp173u19jo8mtw11n3csZ
https://askubuntu.com/questions/59458/error-message-sudo-unable-to-resolve-host-user
 */

/** PHP
参考博客： https://blog.izgq.net/archives/895/
Nginx 本身不支持 PHP 等语言，但是它可以通过 FastCGI 来将请求扔给某些语言或框架处理
配置中将 .php 结尾的请求通过 FashCGI 交给 PHP-FPM 处理，
PHP-FPM是PHP的一个FastCGI管理器

fastcgi_param
一般用法： fastcgi_param parameter value [if_not_empty];
parameter 为当前 fastcgi 协议请求的参数名，value 为 Nginx 要设定此参数的参数值。
这个 value 可以是一个固定的值，也可以是一个变量。
parameter 中有一个参数是最关键的，它就是 SCRIPT_FILENAME，
这个参数定义了这个请求让 PHP-FPM 运行的 php 文件的完整路径，
如果没有它，PHP-FPM 就不知道该运行什么脚本，将会返回一个内容为空白的 200 响应。

fastcgi_param  SCRIPT_FILENAME    $document_root$fastcgi_script_name;
把 SCRIPT_FILENAME 设置为之前用 root 或 alias 设定的路径 + 脚本的相对路径
例子：
假如当前的网站根路径设置为 /var/www/html，
我们访问的 .php 文件的地址是 http://example.com/test/test.php ，
那么，这时候的 $document_root 的值为 /var/www/html ，
$fastcgi_script_name 的值就是 /test/test.php 了。
此时的 SCRIPT_FILENAME 将会被设置为　/var/www/html/test/test.php ，
PHP-FPM 就会按照这个路径读取 php 代码了。

除了最关键的参数外还有一系列的参数需要设置，参考 Nginx 的文档：
https://www.nginx.com/resources/wiki/start/topics/examples/phpfcgi/

Nginx 为我们提供了一个现成的 fastcgi_param 配置的集合，位于 nginx.conf 同目录的
fastcgi_params 和 fastcgi.conf 中
所以，我们在配置 location 时，在 fastcgi_param 的设定上，
我们设置完最关键的 SCRIPT_FILENAME 以后，只需要直接 include fastcgi_params;

下面是一个 location 配置 PHP 的例子：
location ~ \.php$ {
    fastcgi_pass 127.0.0.1:9000;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    include fastcgi_params;
}
~ 表示该 location 使用的是正则表达式匹配，其后 \.php$ 即该正则表达式

fastcgi.conf 是做什么的呢？

fastcgi.conf 和 fastcgi_params 的内容相比，
多了刚刚我们提到的最最关键的一行，其它完全一致
fastcgi_param  SCRIPT_FILENAME    $document_root$fastcgi_script_name;
所以，有了 fastcgi.conf ，我们的配置又可以更简单一些了
location ~ \.php$ {
    fastcgi_pass 127.0.0.1:9000;
    include fastcgi.conf;
}

安全因素：
我们还需要在 nginx 这一层判断一下访问的 PHP 文件是否存在，
避免出现因为 php.ini 开启了 cgi.fix_pathinfo=1 导致任意后缀文件
都能通过 PHP 解释器解析产生的可能引发的安全问题，
虽然这个漏洞在高版本 PHP (>=5.3.9) 已经被补上，但是还是需要注意
这时候我们可以在负责 php 的 location 块增加一个 try_files 来解决
修改后的配置如下：
location ~ \.php$ {
    try_files $uri=404;
    fastcgi_pass 127.0.0.1:9000;
    include fastcgi.conf;
}
 */
