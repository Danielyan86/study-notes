# enable secrets engine
```shell script
vault secrets enable -path=kv kv
Success! Enabled the kv secrets engine at: kv/
(base)
```
## list secrets engines
```shell script
Path          Type         Accessor              Description
----          ----         --------              -----------
cubbyhole/    cubbyhole    cubbyhole_e1363ff1    per-token private secret storage
identity/     identity     identity_cbda967e     identity store
kv/           kv           kv_fdb37ea1           n/a
secret/       kv           kv_22c12bb9           key/value secret storage
sys/          system       system_81744b39       system endpoints used for control, policy and debugging
(base)

```

## disable engine
```shell script
vault secrets disable kv/
Success! Disabled the secrets engine (if it existed) at: kv/
(base)
# admin @ 192 in ~/github_project/study-notes on git:master x [17:35:56]
$ vault secrets list
Path          Type         Accessor              Description
----          ----         --------              -----------
cubbyhole/    cubbyhole    cubbyhole_e1363ff1    per-token private secret storage
identity/     identity     identity_cbda967e     identity store
secret/       kv           kv_22c12bb9           key/value secret storage
sys/          system       system_81744b39       system endpoints used for control, policy and debugging
(base)

```
