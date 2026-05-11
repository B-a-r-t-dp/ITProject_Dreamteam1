# Eigenaar: Bart
# Doel:
# - HTTP-server bouwen op basis van Alpine Linux
# - nginx installeren
# - eigen indexpagina tonen op poort 80

FROM alpine:latest

RUN apk add --no-cache nginx

RUN mkdir -p /run/nginx /usr/share/nginx/html

COPY index.html /usr/share/nginx/html/index.html
COPY default.conf /etc/nginx/http.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
