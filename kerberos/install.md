此文档主要是操作手册，不包括具体概念
# ubuntu install
## 安装
- apt install krb5-kdc krb5-admin-server krb5-config
- 安装过程中需要配置realm（域），KDC，此例子中采用sheldon.com作为realm
- 默认设置两个kdc01，kdc02

![Configuring Kerberos Authentication](https://raw.githubusercontent.com/Danielyan86/xiaoshujiang_images/master/小书匠/1606551157988.png)
![enter description here](https://raw.githubusercontent.com/Danielyan86/xiaoshujiang_images/master/小书匠/1606551659373.png)
![enter description here](https://raw.githubusercontent.com/Danielyan86/xiaoshujiang_images/master/小书匠/1606551685372.png)
- 遇到错误
```shell script
krb5kdc: cannot initialize realm SHELDON.COM - see log file for details
```
因为SHELDON.COM这个域名解析错误造成
修改hosts文件，配置sheldon
sheldon.com 192.168.0.105

- 成功启动服务

```shell script
 systemctl status krb5-kdc.service
● krb5-kdc.service - Kerberos 5 Key Distribution Center
     Loaded: loaded (/lib/systemd/system/krb5-kdc.service; enabled; vendor preset: enabled)
     Active: active (running) since Sat 2020-11-28 16:25:42 CST; 4s ago
    Process: 41412 ExecStart=/usr/sbin/krb5kdc -P /var/run/krb5-kdc.pid $DAEMON_ARGS (code=exited, status=0/SUCCESS)
   Main PID: 41425 (krb5kdc)
      Tasks: 1 (limit: 19009)
     Memory: 1.3M
     CGroup: /system.slice/krb5-kdc.service
             └─41425 /usr/sbin/krb5kdc -P /var/run/krb5-kdc.pid

Nov 28 16:25:42 sheldon krb5kdc[41412]: Setting pktinfo on socket 0.0.0.0.88
Nov 28 16:25:42 sheldon krb5kdc[41412]: Setting up UDP socket for address ::.88
Nov 28 16:25:42 sheldon krb5kdc[41412]: setsockopt(12,IPV6_V6ONLY,1) worked
Nov 28 16:25:42 sheldon krb5kdc[41412]: Setting pktinfo on socket ::.88
Nov 28 16:25:42 sheldon krb5kdc[41412]: Setting up TCP socket for address 0.0.0.0.88
Nov 28 16:25:42 sheldon krb5kdc[41412]: Setting up TCP socket for address ::.88
Nov 28 16:25:42 sheldon krb5kdc[41412]: setsockopt(14,IPV6_V6ONLY,1) worked
Nov 28 16:25:42 sheldon krb5kdc[41412]: set up 6 sockets
Nov 28 16:25:42 sheldon krb5kdc[41425]: commencing operation
Nov 28 16:25:42 sheldon systemd[1]: Started Kerberos 5 Key Distribution Center.
```

## 配置文件修改
确认kdc和admin_server为完整地址
```editorconfig
[realms]
        SHELDON.COM = {
                kdc = kdc02.SHELDON.com
                admin_server = kdc01.SHELDON.com
        }
```

## 添加admin用户
一旦KDC正常运行，则需要一个管理员用户the admin principal。建议使用和平时经常用的用户名有所区别。在终端提示符下输入kadmin.local：
成功之后会进入一个交互式命令行终端，可以通过？查看使用方法。使用 addprinc sheldon/admin命令添加用户,这个地方添加用户之后，安装有kerberos客户端的机器才可以才可以用对应的用户进行第一次验证
```shell script
sudo kadmin.local
[sudo] password for sheldon:
Authenticating as principal root/admin@SHELDON.COM with password.
kadmin.local:  addprinc sheldon/admin
WARNING: no policy specified for sheldon/admin@SHELDON.COM; defaulting to no policy
Enter password for principal "sheldon/admin@SHELDON.COM":
Re-enter password for principal "sheldon/admin@SHELDON.COM":
add_principal: Principal or policy already exists while creating "sheldon/admin@SHELDON.COM".
```

```shell script
admin.local:  ?
Available kadmin.local requests:

add_principal, addprinc, ank
                         Add principal
delete_principal, delprinc
                         Delete principal
modify_principal, modprinc
                         Modify principal
rename_principal, renprinc
                         Rename principal
change_password, cpw     Change password
get_principal, getprinc  Get principal
list_principals, listprincs, get_principals, getprincs
                         List principals
```
接下来，这个新的管理员用户需要有合适的访问控制列表（ACL）权限。它被配置在/etc/krb5kdc/kadm5.acl文件中：

```shell script
 sudo cat /etc/krb5kdc/kadm5.acl
sheldon/admin@SHELDON.COM
```

重启生效
```shell script
sudo service krb5-admin-server restart
```

现在这个新的user principal 可以通过kinit命令进行测试：
```shell script
kinit sheldon/admin -V
Using default cache: /tmp/krb5cc_1000
Using principal: sheldon/admin@SHELDON.COM
Password for sheldon/admin@SHELDON.COM:

Authenticated to Kerberos v5
```

查看获取的ticket
```shell script
klist
Ticket cache: FILE:/tmp/krb5cc_1000
Default principal: sheldon/admin@SHELDON.COM

Valid starting       Expires              Service principal
11/28/2020 22:18:34  11/29/2020 08:18:34  krbtgt/SHELDON.COM@SHELDON.COM
	renew until 11/29/2020 22:18:32

```