# HTTPS Dockerfile
# Verantwoordelijke: Bart
#
# Deze Dockerfile bouwt de HTTPS-servercontainer van onze MVP.
#
# Doel:
# - Alpine Linux gebruiken
# - nginx installeren
# - een self-signed certificaat maken
# - eigen index.html tonen via HTTPS
# - bereikbaar zijn op poort 443

FROM alpine:latest

# Installeert nginx en openssl.
# nginx:
# - webserver die de HTTPS-pagina toont.
# openssl:
# - nodig om tijdens het bouwen een self-signed certificaat te maken.
RUN apk add --no-cache nginx openssl

# Maakt de mappen aan die nginx en het certificaat nodig hebben:
# - /run/nginx voor runtime-bestanden
# - /usr/share/nginx/html voor de websitebestanden
# - /etc/nginx/certs voor het certificaat en de private key
RUN mkdir -p /run/nginx /usr/share/nginx/html /etc/nginx/certs

# Maakt een self-signed certificaat.
# Dit is voldoende voor een demo/MVP.
# Een browser zal dit certificaat niet automatisch vertrouwen,
# maar het toont wel dat HTTPS technisch werkt.
# server.key = private key
# server.crt = certificaat
# C=BE = landcode voor Belgie
# O=Odisee = organisatie
# OU=LaboDashboard ITProject = project/afdeling binnen het certificaat
# CN=localhost = certificaatnaam voor lokale testomgeving
RUN openssl req -x509 -nodes -days 365 \
    -newkey rsa:2048 \
    -keyout /etc/nginx/certs/server.key \
    -out /etc/nginx/certs/server.crt \
    -subj "/C=BE/O=Odisee/OU=LaboDashboard ITProject/CN=localhost"

# Kopieert onze eenvoudige HTTPS-testpagina naar de nginx webroot.
COPY index.html /usr/share/nginx/html/index.html

# Kopieert onze nginx-configuratie voor HTTPS.
# Daarin staat dat nginx poort 443 gebruikt
# en waar het certificaat en de key staan.
COPY default.conf /etc/nginx/http.d/default.conf

# Documenteert dat deze container poort 443 gebruikt.
EXPOSE 443

# Start nginx op de voorgrond zodat de container actief blijft.
CMD ["nginx", "-g", "daemon off;"]
