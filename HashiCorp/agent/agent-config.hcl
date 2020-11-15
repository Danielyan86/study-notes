pid_file = "./pidfile"

vault {
   address = "http://127.0.0.1:8200" # server地址
}

auto_auth {
   method "approle" {
       mount_path = "auth/approle"  # 验证方法
       config = {
           role_id_file_path = "roleid"
           secret_id_file_path = "secretid"
           remove_secret_id_file_after_reading = false
       }
   }

   # 验证成功之后，token会写入sink配置的文件
   sink "file" {
       config = {
           path = "approleToken"
       }
   }
}

# 根据定义模板进行渲染
template {
  source      = "./customer.tmpl"
  destination = "./customer.txt"
}