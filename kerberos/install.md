# ubuntu install
- apt install krb5-kdc krb5-admin-server krb5-config
- 安装过程中需要配置realm（域），KDC，
![Configuring Kerberos Authentication](https://raw.githubusercontent.com/Danielyan86/xiaoshujiang_images/master/小书匠/1606551157988.png)
![enter description here](https://raw.githubusercontent.com/Danielyan86/xiaoshujiang_images/master/小书匠/1606551659373.png)
![enter description here](https://raw.githubusercontent.com/Danielyan86/xiaoshujiang_images/master/小书匠/1606551685372.png)
- 成功启动服务

```
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


# 客户端配置
