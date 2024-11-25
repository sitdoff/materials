FROM nginx:1.27.2-alpine

LABEL creator="Roman Ivanov"
LABEL email="sitdoff@gmail.com"

RUN rm /etc/nginx/conf.d/default.conf
COPY materials.conf /etc/nginx/conf.d/
