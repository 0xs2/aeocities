# aeocities

**aeocities** is an unofficial API for 'neocities'

* Tiny Web UI: `/` 
* Site list: `/list/[#]` 
* Random Site: `/random`
* Site information: `/site/[site]`

### Install and run

`pip3 install beautifulsoup4 flask re random string`
`cd aeocities/ && screen -dmS python3 main.py`

### Nginx config
```
server {

    listen 80;
    listen [::]:80;

    server_name aeocites.example.org www.aeocites.example.org;

    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";
    add_header Referrer-Policy "no-referrer";
    add_header Content-Security-Policy "script-src 'self'; object-src 'self'";
    add_header Strict-Transport-Security "max-age=15768000; includeSubdomains";
    add_header Feature-Policy "accelerometer 'none'; camera 'none'; geolocation 'none'; gyroscope 'none'; magnetometer 'none'; microphone 'none'; payment 'none'; usb 'none'";

    location / {
        proxy_pass http://localhost:5050;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
    }
}
```
