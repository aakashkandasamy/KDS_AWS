upstream ws-backend {
server <Private IP>:8501;
}
server {
    listen 80; 
    server_name <Private IP>;
location / {
proxy_pass http://ws-backend;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header Host $http_host;
      proxy_redirect off;
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "upgrade";
    }
  }
