# Eigenaar: Bart
# Doel:
# - centrale Flask-server bouwen als eigen Alpine Docker-image
# - Python, Flask en Ansible beschikbaar maken in de container
# - container starten met app.py

FROM python:3.12-alpine

WORKDIR /app

RUN apk add --no-cache openssh-client sshpass

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
