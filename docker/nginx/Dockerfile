FROM nginx:latest

RUN rm /etc/nginx/conf.d/*

COPY ./nginx.conf /etc/nginx/conf.d/nginx.conf
COPY ./proxy.conf /etc/nginx/conf.d/proxy.conf
