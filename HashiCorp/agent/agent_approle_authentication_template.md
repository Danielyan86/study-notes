# 参考链接
- https://learn.hashicorp.com/tutorials/vault/agent-templates?in=vault/app-integration
- https://learn.hashicorp.com/tutorials/vault/approle?in=vault/auth-methods
# 步骤
## 数据准备
把 data.json 里面数据写入vault
```shell script
vault kv put secret/customers/acme @data.json
$ vault kv put secret/customers/acme @data.json
Key              Value
---              -----
created_time     2020-11-15T13:27:36.954369Z
deletion_time    n/a
destroyed        false
version          2

## 验证写入的secret
vault kv get secret/customers/acme
====== Metadata ======
Key              Value
---              -----
created_time     2020-11-15T13:27:36.954369Z
deletion_time    n/a
destroyed        false
version          2

======== Data ========
Key              Value
---              -----
contact_email    james@acme.com
customer_id      ABXX2398YZPIE7391
organization     ACME Inc.
region           US-West
status           active
type             premium
zip_code         94105
(base)
```

## approle 验证方法准备
### 为app创建策略文件并上传 app-pol.hcl
```shell script
vault policy write app-pol app-pol.hcl
Success! Uploaded policy: app-pol
```

## 创建一个应用角色role, 并对其使用刚创建的策略app-pol
```shell script
vault write auth/approle/role/apps policies="app-pol"
Success! Data written to: auth/approle/role/apps
```

## 读取roleID 和secretID 并写入文件
```shell script
vault read -format=json auth/approle/role/apps/role-id | jq  -r '.data.role_id' > roleID
vault write -f -format=json auth/approle/role/apps/secret-id | jq -r '.data.secret_id' > secretID

```

## 检查配置文件
agent-config.hcl

## 启动agent
```shell script
vault agent -config=agent-config.hcl -log-level=debug
==> Vault agent started! Log data will stream in below:

==> Vault agent configuration:
......

2020/11/15 14:53:36.786622 [DEBUG] (runner) was not watching 1 dependencies
2020/11/15 14:53:36.786627 [DEBUG] (watcher) adding vault.read(secret/data/customers/acme)
2020/11/15 14:53:36.786644 [DEBUG] (runner) diffing and updating dependencies
2020/11/15 14:53:36.786650 [DEBUG] (runner) watching 1 dependencies
2020-11-15T22:53:36.788+0800 [INFO]  auth.handler: renewed auth token
2020/11/15 14:53:36.902282 [DEBUG] (runner) receiving dependency vault.read(secret/data/customers/acme)
2020/11/15 14:53:36.902338 [DEBUG] (runner) initiating run
2020/11/15 14:53:36.902349 [DEBUG] (runner) checking template 56ba7f3e29857b85850ab5e0eb1151a3
2020/11/15 14:53:36.902947 [DEBUG] (runner) rendering "./customer.tmpl" => "./customer.txt"
2020/11/15 14:53:36.904116 [DEBUG] (runner) diffing and updating dependencies
2020/11/15 14:53:36.904141 [DEBUG] (runner) vault.read(secret/data/customers/acme) is still needed
2020/11/15 14:53:36.904162 [DEBUG] (runner) watching 1 dependencies
2020/11/15 14:53:36.904170 [DEBUG] (runner) all templates rendered

```
根据输出日志可以看到，自动验证通过之后，会根据模板渲染日志（rendering "./customer.tmpl" => "./customer.txt"）。

## 验证agent功能
新开一个终端，更新secret内容
```
$ vault kv patch secret/customers/acme contact_email=dongdong@fk.com
Key              Value
---              -----
created_time     2020-11-15T14:59:04.279827Z
deletion_time    n/a
destroyed        false
version          4
(base)
```

确认更新成功之后，agent大概在5分钟内会自动重新渲染模板内容
```
$ vault kv get secret/customers/acme
====== Metadata ======
Key              Value
---              -----
created_time     2020-11-15T15:01:48.773294Z
deletion_time    n/a
destroyed        false
version          6

======== Data ========
Key              Value
---              -----
contact_email    dongdong@fk.com
customer_id      ABXX2398YZPIE7391
organization     ACME Inc.
region           US-West
status           active
type             premium
zip_code         94105
(base)
```

agent终端日志会重新刷新
```shell script
2020/11/15 15:02:38.027329 [DEBUG] (runner) receiving dependency vault.read(secret/data/customers/acme)
2020/11/15 15:02:38.027357 [DEBUG] (runner) initiating run
2020/11/15 15:02:38.027373 [DEBUG] (runner) checking template 56ba7f3e29857b85850ab5e0eb1151a3
2020/11/15 15:02:38.027974 [DEBUG] (runner) rendering "./customer.tmpl" => "./customer.txt"
2020/11/15 15:02:38.068176 [INFO] (runner) rendered "./customer.tmpl" => "./customer.txt"
2020/11/15 15:02:38.068210 [DEBUG] (runner) diffing and updating dependencies
2020/11/15 15:02:38.068222 [DEBUG] (runner) vault.read(secret/data/customers/acme) is still needed
2020/11/15 15:02:38.068242 [DEBUG] (runner) watching 1 dependencies
2020/11/15 15:02:38.068250 [DEBUG] (runner) all templates rendered
```