# Eigenaar: Bart
# Doel:
# - FTP-server bouwen op basis van Alpine Linux
# - FTP-gebruiker en testbestand voorzien
# - FTP beschikbaar maken op poort 20/21

FROM alpine:latest

RUN apk add --no-cache vsftpd

RUN adduser -D ftpuser && echo "ftpuser:itproject" | chpasswd
RUN mkdir -p /home/ftpuser/ftp /etc/vsftpd && echo "ITProject FTP testbestand" > /home/ftpuser/ftp/test.txt

COPY vsftpd.conf /etc/vsftpd/vsftpd.conf

EXPOSE 20 21

CMD ["vsftpd", "/etc/vsftpd/vsftpd.conf"]
