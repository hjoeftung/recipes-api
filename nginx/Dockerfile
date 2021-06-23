FROM nginx:latest

COPY nginx.conf /etc/nginx/nginx.conf
COPY 51.116.177.181.pem 51.116.177.181-key.pem /etc/ssl/certs/
COPY 51.116.177.181-client.pem 51.116.177.181-client-key.pem /etc/nginx/

WORKDIR .