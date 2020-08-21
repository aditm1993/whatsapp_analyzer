# Django Deployment to Ubuntu 20.04 on AWS EC2

These steps should work on any previous or future version of ubuntu as well
on EC2, the username is ubuntu. on other vps, replace it will the appropriate username 

# Software

#### Update packages

```
# sudo apt update
# sudo apt upgrade
```

## Install Python 3, Postgres & NGINX

```
# sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl
```

# Vitrual Environment

You need to install the python3-venv package

```
# sudo apt install python3-venv
```

### Create project directory

```
# mkdir pyapps
# cd pyapps
```

### Create venv

```
# python3 -m venv ./venv
```

### Activate the environment

```
# source venv/bin/activate
```

# Git & Upload

### Clone the project into the app folder on your server

```
# git clone https://github.com/royz/whatsapp_analyzer.git
```

## Install pip modules from requirements

You could manually install each one as well

```
# pip install -r requirements.txt
```

## Run Migrations

```
# python manage.py makemigrations
# python manage.py migrate
```

## Create static files

```
python manage.py collectstatic
```

## Run Server on port 8000 for testing

```
# python manage.py runserver 0.0.0.0:8000
```

### Test the site at YOUR_SERVER_IP:8000

Add some data in the admin area

# Gunicorn Setup

Install gunicorn

```
# pip install gunicorn
```

### Test Gunicorn serve

```
# gunicorn --bind 0.0.0.0:8000 whatsapp_analyzer.wsgi
```

### Stop server & deactivate virtual env

```
ctrl-c
# deactivate
```

### open settings.py file under `whatsapp_analyzer/whatsapp_analyzer/`
```
# nano whatsapp_analyzer/whatsapp_analyzer/settings.py
```
then make the folowing changes
```python
DEBUG = False
ALLOWED_HOSTS = ['<your-server-ip-address>']
```

### Open gunicorn.socket file

```
# sudo nano /etc/systemd/system/gunicorn.socket
```

### Copy this code, paste it in and save

```
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

### Open gunicorn.service file

```
# sudo nano /etc/systemd/system/gunicorn.service
```

### Copy this code, paste it in and save

```
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/pyapps/whatsapp_analyzer
ExecStart=/home/ubuntu/pyapps/venv/bin/gunicorn \
          --access-logfile - \
          --timeout 3600 \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          whatsapp_analyzer.wsgi:application

[Install]
WantedBy=multi-user.target
```

### Start and enable Gunicorn socket

```
# sudo systemctl start gunicorn.socket
# sudo systemctl enable gunicorn.socket
```

### Check status of guinicorn

```
# sudo systemctl status gunicorn.socket
```

### Check the existence of gunicorn.sock

```
# file /run/gunicorn.sock
```

# NGINX Setup

### Create project folder

```
# sudo nano /etc/nginx/sites-available/whatsapp_analyzer
```

### Copy this code and paste into the file

```
server {
    listen 80;
    server_name <server-ip-address>;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/ubuntu/pyapps/whatsapp_analyzer;
    }

    location /media/ {
        root /home/ubuntu/pyapps/whatsapp_analyzer;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

### Enable the file by linking to the sites-enabled dir

```
# sudo ln -s /etc/nginx/sites-available/whatsapp_analyzer /etc/nginx/sites-enabled
```

### Test NGINX config

```
# sudo nginx -t
```


### Reload NGINX & Gunicorn

```
# sudo systemctl restart nginx
# sudo systemctl restart gunicorn
```
