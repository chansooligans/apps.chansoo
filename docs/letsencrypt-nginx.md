# Using Free Let’s Encrypt SSL/TLS Certificates with NGINX

https://www.nginx.com/blog/using-free-ssltls-certificates-from-lets-encrypt-with-nginx/

```
$ apt-get update
$ sudo apt-get install certbot
$ apt-get install python3-certbot-nginx
```

```
sudo certbot --nginx -d tailoredscoops.com -d apps.chansoos.com
```