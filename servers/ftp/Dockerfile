# FTP Dockerfile
# Verantwoordelijke: Bart
#
# Deze Dockerfile bouwt de FTP-servercontainer van onze MVP.
#
# Doel:
# - Alpine Linux gebruiken
# - vsftpd installeren
# - een testgebruiker voorzien
# - een testbestand klaarzetten
# - FTP beschikbaar maken op poort 20 en 21

FROM alpine:latest

# Installeert vsftpd.
# vsftpd is de FTP-server die in deze container draait.
# --no-cache houdt de image kleiner doordat Alpine geen package-cache bewaart.
RUN apk add --no-cache vsftpd

# Maakt een eenvoudige FTP-testgebruiker aan.
#
# Gebruiker:
# - ftpuser
#
# Wachtwoord:
# - itproject
#
# Dit is alleen bedoeld voor de MVP/demo.
# Voor productie zou je dit niet hardcoded in een Dockerfile zetten.
RUN adduser -D ftpuser && echo "ftpuser:itproject" | chpasswd

# Maakt een FTP-map aan voor de testgebruiker
# en zet er een klein testbestand in.
# Zo kunnen we later controleren of FTP effectief werkt
# door met ftpuser in te loggen en test.txt op te vragen.
RUN mkdir -p /home/ftpuser/ftp \
    && echo "ITProject FTP testbestand" > /home/ftpuser/ftp/test.txt \
    && chown -R ftpuser:ftpuser /home/ftpuser/ftp

# Kopieert de vsftpd-configuratie naar de juiste plaats in de container.
COPY vsftpd.conf /etc/vsftpd/vsftpd.conf

# Documenteert de FTP-poorten.
# Poort 21:
# - commandokanaal voor FTP.
# Poort 20:
# - traditioneel datakanaal bij active FTP.
EXPOSE 20 21

# Start de FTP-server met onze configuratie.
CMD ["vsftpd", "/etc/vsftpd/vsftpd.conf"]
