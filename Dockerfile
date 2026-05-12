# Flask Dockerfile
# Verantwoordelijke: Bart
#
# Deze Dockerfile bouwt de container voor onze centrale Flask-applicatie.
# Dit is dus de webapp waar de docent later kan inloggen,
# een netwerkopstelling kan kiezen en een configuratie kan starten.
#
# We gebruiken een Alpine-gebaseerde Python-image omdat de opdracht vraagt
# om lichte Linux-images en omdat Alpine klein en duidelijk is.

FROM python:3.12-alpine

# Alle projectbestanden komen in de container in de map /app.
# Vanaf hier worden commando's standaard in /app uitgevoerd.

WORKDIR /app

# Deze pakketten zijn nodig voor de Ansible/SSH-kant van het project.
#
# openssh-client:
# - nodig om via SSH met routers/switches te verbinden.
#
# sshpass:
# - handig voor testopstellingen waar met username/password gewerkt wordt,
#   zoals vaak in EVE-NG-labo's.
#
# --no-cache:
# - zorgt dat Alpine geen onnodige package-cache bewaart,
#   waardoor de image kleiner blijft.

RUN apk add --no-cache openssh-client sshpass

# Eerst kopiëren we alleen requirements.txt.
# Daarna installeren we de Python-packages.
#
# Dit is handig omdat Docker deze stap kan cachen:
# als alleen app.py wijzigt maar requirements.txt niet,
# moeten de packages niet telkens opnieuw geïnstalleerd worden.

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Nu kopiëren we de rest van het project naar de container.
# Dit bevat onder andere:
# - app.py
# - templates/
# - static/
# - modules/
# - ansible/
# - database/

COPY . .

# Flask draait in ons project op poort 5000.
# EXPOSE opent de poort niet automatisch op de host,
# maar documenteert welke poort de container gebruikt.
# docker-compose.yml koppelt deze poort later aan de host.

EXPOSE 5000

# Start de Flask-applicatie wanneer de container opstart.
# app.py bevat onderaan app.run(host="0.0.0.0", port=5000),
# zodat Flask bereikbaar is van buiten de container.

CMD ["python", "app.py"]
