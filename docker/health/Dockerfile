FROM ubuntu:latest

RUN apt -y update && apt -y upgrade && apt -y install nginx && apt -y install curl 

RUN echo "\ndaemon off;" >> /etc/nginx/nginx.conf

COPY index.html /usr/share/nginx/html

HEALTHCHECK --interval=10s --timeout=3 CMD curl -f http://localhost/ || exit 1

CMD ["nginx"]
