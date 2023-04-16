# MySql

cat $HOME/bitnami_application_password  
mysql -u root -p
CREATE USER 'user'@'127.0.0.1' IDENTIFIED BY 'password';  
GRANT ALL PRIVILEGES ON apps.* TO 'user'@'127.0.0.1';  

CREATE USER 'user'@'localhost' IDENTIFIED BY 'password';  
GRANT ALL PRIVILEGES ON apps.* TO 'user'@'localhost';  