# 教程文档
https://learn.hashicorp.com/tutorials/vault/getting-started-dev-server

## 安装
### mac 环境安装 
- brew install hashicorp/tap/vault
- 确认结果
```shell script
vault
Usage: vault <command> [args]

Common commands:
    read        Read data and retrieves secrets
    write       Write data, configuration, and secrets
    delete      Delete secrets and configuration
    list        List data or secrets
    login       Authenticate locally
    agent       Start a Vault agent
    server      Start a Vault server
    status      Print seal and HA status
    unwrap      Unwrap a wrapped secret

```

### 启动服务
需要注意终端会生成一个root token。后面的认证需要用到
```shell script
vault server -dev
==> Vault server configuration:

             Api Address: http://127.0.0.1:8200
                     Cgo: disabled
         Cluster Address: https://127.0.0.1:8201
              Go Version: go1.14.7
              Listener 1: tcp (addr: "127.0.0.1:8200", cluster address: "127.0.0.1:8201", max_request_duration: "1m30s", max_request_size: "33554432", tls: "disabled")
               Log Level: info
                   Mlock: supported: false, enabled: false
           Recovery Mode: false
                 Storage: inmem
                 Version: Vault v1.5.3
             Version Sha: 9fcd81405feb320390b9d71e15a691c3bc1daeef

WARNING! dev mode is enabled! In this mode, Vault runs entirely in-memory
and starts unsealed with a single unseal key. The root token is already
authenticated to the CLI, so you can immediately begin using Vault.

You may need to set the following environment variable:

    $ export VAULT_ADDR='http://127.0.0.1:8200'

The unseal key and root token are displayed below in case you want to
seal/unseal the Vault or re-authenticate.

Unseal Key: OpNnSdE4Pi2O8z5yZ0893aXSm2GkdyPLbcRxxsNLEWQ=
Root Token: s.hH4HEhn1yeJgY5qYPV6SbkWI

Development mode should NOT be used in production installations!

==> Vault server started! Log data will stream in below:
```
- 添加环境变量
```shell script
# 此处的token来自于启动时候终端生成的值
export VAULT_TOKEN="s.hH4HEhn1yeJgY5qYPV6SbkWI"
export VAULT_ADDR='http://127.0.0.1:8200'
```
## 写入秘钥
- 添加键值对
同样的key 再次输入之后version版本会自动加一
```
vault kv put secret/hello foo=world
Key              Value
---              -----
created_time     2020-09-20T09:41:43.402202Z
deletion_time    n/a
destroyed        false
version          2
(base)
# admin @ aDong in ~ [17:41:43]
$ vault kv put secret/hello foo=world
Key              Value
---              -----
created_time     2020-09-20T09:41:45.700426Z
deletion_time    n/a
destroyed        false
version          3
```
- 获取
```shell script
vault kv get secret/hello
====== Metadata ======
Key              Value
---              -----
created_time     2020-09-20T09:41:45.700426Z
deletion_time    n/a
destroyed        false
version          3

=== Data ===
Key    Value
---    -----
foo    world
(base)
```
- 获取固定key-value
```shell script
vault kv put secret/hello foo=world excited=yes
Key              Value
---              -----
created_time     2020-09-20T09:45:50.793237Z
deletion_time    n/a
destroyed        false
version          4
(base)
# admin @ aDong in ~ [17:45:50]
$ vault kv get -field=excited secret/hello
yes
```

- 删除key-value
```
vault kv delete secret/hello

Success! Data deleted (if it existed) at: secret/hello
(base)
```