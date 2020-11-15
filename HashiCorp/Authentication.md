# 默认验证方式
通过dev模式启动的vault默认认证方式是token，终端会显示一个默认的token和使用方法
```
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

Unseal Key: JJ+7bVXhNLO5qc4cfIMX8XiU/rzelhJ47E9CKe6tVUw=
Root Token: s.PNXTWmIzbLGLW72cYXaoEIsI

Development mode should NOT be used in production installations!
```
在重新打开一个新的终端之后，根据提示方法给环境变量赋值，相当用默认验证方法给客户端做认证
```shell script
export VAULT_TOKEN="s.PNXTWmIzbLGLW72cYXaoEIsI"
export VAULT_ADDR='http://127.0.0.1:8200'
```
除了默认的token认证之外，vault还支持别的很多种加密方式，比如approle，阿里云，k8s，LDAP等等
## 添加新的认证方式
###  AppRole

新加一个approle的认证
```shell script
vault auth enable approle
Success! Enabled approle auth method at: approle/
(base)
```
然后通过auth list命令可以查看已经存在的认证方式,可以看到有一个默认的auth_approle_5d1aa63a
```
vault auth list
Path        Type       Accessor                 Description
----        ----       --------                 -----------
approle/    approle    auth_approle_5d1aa63a    n/a
token/      token      auth_token_278caa58      token based credentials
(base)
```
#### 新加一个role
添加一个role，叫my-role
```shell script
vault write auth/approle/role/my-role \
    secret_id_ttl=1000m \
    token_num_uses=100 \
    token_ttl=200m \
    token_max_ttl=300m \
    secret_id_num_uses=400
Success! Data written to: auth/approle/role/my-role
```
读取新添加的role-id
```shell script
vault read auth/approle/role/my-role/role-id

Key        Value
---        -----
role_id    59bc028a-b24a-a36a-a8c7-82a1c9f54fa5
```
为新的my-role生成secret id
```shell script
 vault write -f auth/approle/role/my-role/secret-id
Key                   Value
---                   -----
secret_id             3ca5adbc-711b-5026-fa64-b45023e44678
secret_id_accessor    e9b737fa-0d93-240b-a00c-8c69d297c730
```
把新生成的secret_id和role_id写入认证里面，需要注意是role_id和secret_id配对，不是和secret_id_accessor配对
```shell script
vault write auth/approle/login \
    role_id=59bc028a-b24a-a36a-a8c7-82a1c9f54fa5 \
    secret_id=b5a5360c-bb47-71a6-9c7f-8b7479afa9e1
Key                     Value
---                     -----
token                   s.ULxTLUhCG5sDWqWMzstjJlRT
token_accessor          b7K8QSVXEHayjo5v4dG2nSL2
token_duration          20m
token_renewable         true
token_policies          ["default"]
identity_policies       []
policies                ["default"]
token_meta_role_name    my-role
```


这个时候得到了一对新的role_id和secret_id
然后我们再新开一个窗口，采用*APProle*的方式来进行认证


### cli 方式
默认路径approle，如果需要改变path，指定auth/my-path/login 替换掉

### agent 认证

