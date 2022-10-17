# Vue web backend api

Solar vue web backend api program
AUTHOR : YUSHAN

<br>

---

## Environment Variable
* Require means program won't run if variable missing.

Name                      | Description                                             | Require  | Default                         |
------------------------- | ------------------------------------------------------  | -------- | ------------------------------- |
web_backend_secret_key    | Flask app secret key                                    | ✓        |                                 |
web_backend_project_name  | Specify Frontend Version is "99M" or "taipower"         |          | 99M                             |
web_backend_login_enable  | Set "true" enable website auth. For 99M set "false"     |          | false                           |
static_file_path          | path of static folder                                   |          | /usr/share/nginx/solar_static/  |
MONGODB_HOSTNAME          | MongoDB Hostname. For Replica Set, use 'ip1,ip2,ip3'    |          | localhost                       |
MONGODB_PORT              | MongoDB Port. For Replica Set, use 'port1,port2,port3'|          | 27017                           |
MONGODB_USERNAME          | MongoDB Username                                        |          | root                            |
MONGODB_PASSWORD          | MongoDB password                                        |          | pc152                           |
MONGODB_RS_NAME           | MongoDB Replica Set Name                                |          | rs0                             |
ir_image_server_ip        | Hostname or IP of IR image processing server            |          | http://140.118.172.245:5000     |
oidc_github_client_id     | Client_id of github for open id connect                 |          | ""                              |
oidc_github_client_secret | Client_secret of github for open id connect             |          | ""                              |

<br>

**Environment Variables Used In Related Library**

Name                      | Description                                             | Require  | Default                         |
------------------------- | ------------------------------------------------------  | -------- | ------------------------------- |
FILE_PATH | Used in week_A_excel Library developed by Ryan. The path where report prototype saved. If not set, will use a default one in week_A_excel/ |   | init_config


**Detail on** ***web_backend_project_name***

Compare to 99M Vue (ES Ver.), Taipower Vue is more complicated (AI, Dispatch, and more new features).
To maximize sharing same API between two vue programs, I use Flask Blueprint.

All API view_functions or endpoints are moved out of app.py and distributd to separate files.
1. For common API and function both 99M and taipower will use, __app_common.py__
2. For 99M specified, __app_99M.py__
3. For Taipower specified, __app_taipower.py__

<br>

---

## Nginx Configuration
### Vue
1. debug
```
location / {
    rewrite ^/^/ /$1 break;
    proxy_pass http://localhost:8080/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}
```
2. production, built
```
location / {
    root /usr/share/nginx/taipower_vue;     #directory where index.html at
    try_files $uri /index.html;
}
```
### solar-vue-web-backend api
```
location /api/ {
    proxy_pass http://localhost:8000/;     #api url   
    tcp_nodelay on;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}    
```
### solar_static
1. without ahthentication
```
location /solar_static/ {
    alias /Users/sam/Documents/solar/ysolar/solar_static/; 
}
```
2. optional, with authentication
* a subrequest will be sent to /api/solar_static_auth, access denied when response code equals to 401 or 403.
```
location /solar_static/ {
    auth_request /api/solar_static_auth;
    alias /Users/sam/Documents/solar/ysolar/solar_static/; 
}
```
* And then, modify location /api/
```
location /api/ {
    proxy_pass http://localhost:8000/;     #api url   
    tcp_nodelay on;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        
    #For solar_static authentication
    location /api/solar_static_auth {
        internal;
        set $query '';
        if ($request_uri ~* "[^\?]+\?(.*)$") {
                set $query $1;
        }
        proxy_pass http://localhost:8000/solar_static_auth?$query;     # Remember to change port
    }
}    
```
<br>

---

## Running Gunicorn
> The number of worker processes
Command line: `-w NUMBER`
```
$ gunicorn -w 3 --bind 0.0.0.0:8088 wsgi
```
<br>

> Debugging
Command line: `--reload`
```
$ gunicorn -w 3 --reload --bind 0.0.0.0:8088 wsgi
```
<br>

> Logging
Command line: `--access-logfile FILE`
```
$ gunicorn -w 3 --access-logfile ~/Dec_05.log --bind 0.0.0.0:8088 wsgi
```
<br>

---
## Docker Build and Run before pushing to gitlab
```
docker build -t solar-vue-web-backend .
```
```
docker run -e WORKERS='3' -e APP_PORT='80' -e web_backend_secret_key="test_key" -e MONGODB_HOSTNAME="MONGODB_HOSTNAME" -e web_backend_project_name="taipower" -p 8000:80  solar-vue-web-backend
```
* Adjust environment variables and port as needed
