# HTTP Dockerfile
# Verantwoordelijke: Bart
#
# Deze Dockerfile bouwt de HTTP-servercontainer van onze MVP.
#
# Doel:
# - Alpine Linux gebruiken
# - nginx installeren
# - eigen index.html tonen
# - bereikbaar zijn op poort 80

FROM alpine:latest

# Installeert nginx.
# --no-cache zorgt ervoor dat er geen onnodige package-cache in de image blijft.
RUN apk add --no-cache nginx

# Maakt de mappen aan die nginx nodig heeft:
# - /run/nginx voor runtime-bestanden
# - /usr/share/nginx/html voor de websitebestanden
RUN mkdir -p /run/nginx /usr/share/nginx/html

# Kopieert onze eenvoudige testpagina naar de standaard webroot van nginx.
COPY index.html /usr/share/nginx/html/index.html

# Kopieert onze nginx-configuratie.
# Daarin staat dat nginx moet luisteren op poort 80.
COPY default.conf /etc/nginx/http.d/default.conf

# Documenteert dat deze container poort 80 gebruikt.
EXPOSE 80

# Start nginx op de voorgrond.
# Dat is nodig in Docker: als nginx op de achtergrond draait,
# stopt de container meteen.
CMD ["nginx", "-g", "daemon off;"]
