pid_file = "./pidfile"

vault {
   address = "http://127.0.0.1:8200"
}

auto_auth {
   method "approle" {
       mount_path = "auth/approle"
       config = {
           role_id_file_path = "roleid"
           secret_id_file_path = "secretid"
           remove_secret_id_file_after_reading = false
       }
   }


}

template {
  source      = "./customer.tmpl"
  destination = "./customer.txt"
}