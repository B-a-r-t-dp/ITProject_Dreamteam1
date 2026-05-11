# Eigenaar: Bart
# Doel:
# - HTTPS-server bouwen op basis van Alpine Linux
# - nginx en self-signed certificaat voorzien
# - eigen indexpagina tonen op poort 443

FROM alpine:latest

RUN apk add --no-cache nginx openssl

RUN mkdir -p /run/nginx /usr/share/nginx/html /etc/nginx/certs

RUN openssl req -x509 -nodes -days 365 \
    -newkey rsa:2048 \
    -keyout /etc/nginx/certs/server.key \
    -out /etc/nginx/certs/server.crt \
    -subj "/CN=localhost"

COPY index.html /usr/share/nginx/html/index.html
COPY default.conf /etc/nginx/http.d/default.conf

EXPOSE 443

CMD ["nginx", "-g", "daemon off;"]
