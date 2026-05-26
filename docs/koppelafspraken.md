# Koppelafspraken

## Waarom dit document?

Iedereen werkt aan een eigen deel, maar de delen moeten na elke sprint samen blijven werken.

Daarom spreken we vaste structuren af:

- welke tabellen SQLite heeft;
- welke functies de backend aanbiedt;
- welk formaat Ansible teruggeeft;
- welke data Flask aan templates doorgeeft;
- welke containers Docker Compose aanbiedt.

## 1. SQLite-structuur

Joost werkt in:

```text
database/schema.sql
modules/database_tools.py
```

SQLite bevat minimaal deze tabellen.

### users

Doel: docenten opslaan.

| Veld | Betekenis |
| --- | --- |
| `id` | Uniek nummer van de gebruiker. |
| `username` | Loginnaam van de docent. |
| `password_hash` | Gehasht wachtwoord. Geen plaintext. |
| `role` | Rol, bijvoorbeeld `teacher`. |

### network_setups

Doel: beschikbare netwerkopstellingen opslaan.

| Veld | Betekenis |
| --- | --- |
| `id` | Uniek nummer van de opstelling. |
| `name` | Naam die de docent ziet. |
| `description` | Korte uitleg van de opstelling. |
| `playbook_data` | Info waarmee Bart weet welke Ansible-flow hoort bij deze opstelling. |

### deployment_logs

Doel: Ansible-uitvoeringen bewaren.

| Veld | Betekenis |
| --- | --- |
| `id` | Uniek nummer van de logregel. |
| `user_id` | Welke docent de actie startte. |
| `setup_id` | Welke netwerkopstelling gestart werd. |
| `timestamp` | Wanneer de actie gebeurde. |
| `status` | `success` of `failed`. |
| `output` | Tekstuele output of foutmelding. |

## 2. Vaste Python-functies

### Joost - database_tools.py

### `get_deployment_logs_for_user(user_id, limit=10)`

Deze functie geeft de laatste deployment logs terug voor een specifieke gebruiker/docent.

Deze functie is toegevoegd voor PB-66, zodat we kunnen controleren welke docent welke configuratie gestart heeft.

Returnformaat:

```python
[
    {
        "id": 1,
        "user_id": 1,
        "setup_id": 1,
        "timestamp": "2026-05-19 09:08:38",
        "status": "success",
        "output": "Ansible-output of foutmelding"
    }
]
```
`verify_user()` geeft bij succes dit formaat terug:

```python
{
    "id": 1,
    "username": "docent",
    "role": "teacher"
}
```

Bij mislukte login:

```python
None
```

`get_network_setups()` geeft dit formaat terug:

```python
[
    {
        "id": 1,
        "name": "Basisopstelling",
        "description": "1 router, 1 switch, HTTP, HTTPS en FTP",
        "playbook_data": "setup1",
        "info": {
            "name": "Basisopstelling",
            "description": "1 router, 1 switch, HTTP, HTTPS en FTP",
            "devices": {},
            "variables": {}
        }
    }
]
```

`playbook_data` verwijst voorlopig naar de map onder `ansible/playbooks/`.
Voor de basisopstelling is dat dus:

```text
setup1
```

De extra sleutel `info` komt uit:

```text
ansible/playbooks/setup1/info.yml
```

Die informatie mag op het dashboard getoond worden. Zo moet Lina geen netwerkdetails hardcoded in HTML zetten.

### Bart - ansible_tools.py

Deze functie moet bestaan:

```python
run_setup(setup_id, logged_user=None)
```

Die geeft altijd dit formaat terug:

```python
{
    "status": "success",
    "output": "Ansible-output..."
}
```

Of bij fout:

```python
{
    "status": "failed",
    "output": "Foutmelding..."
}
```

Belangrijk: de sleutels moeten altijd `status` en `output` zijn.

`logged_user` is optioneel.
Flask geeft hier de aangemelde username mee, bijvoorbeeld `docent` of `docent2`.
Ansible gebruikt die waarde alleen om backupbestanden herkenbaar te maken.
De echte koppeling met de gebruiker blijft in SQLite via `deployment_logs.user_id`.

### Afspraak outputformaat Ansible -> Flask -> SQLite

`modules/ansible_tools.py` is verantwoordelijk voor het starten van de Ansible-flow.
Flask mag dus niet zelf rechtstreeks `ansible-playbook` starten.

Flask roept alleen deze functie aan:

```python
result = run_setup(setup_id, logged_user=username)
```

Die functie geeft altijd een dictionary terug met exact deze sleutels:

```python
{
    "status": "success",
    "output": "tekstuele output van Ansible"
}
```

Bij een fout geeft de functie:

```python
{
    "status": "failed",
    "output": "foutmelding of Ansible stderr"
}
```

| Sleutel | Type | Toegelaten waarden | Betekenis |
| --- | --- | --- | --- |
| `status` | string | `success` of `failed` | Geeft aan of de Ansible-flow gelukt is. |
| `output` | string | vrije tekst | Output of foutmelding die op het dashboard getoond en in SQLite opgeslagen wordt. |

Belangrijk:

- `status` gebruikt altijd kleine letters: `success` of `failed`;
- gebruik dus geen `SUCCESS`, `FAILED` of `ERROR`;
- `output` is altijd tekst, ook als Ansible geen output teruggeeft;
- de sleutels `status` en `output` mogen niet gewijzigd worden zonder teamoverleg.

Voorbeeld voor Flask:

```python
result = run_setup(setup_id, logged_user=session["username"])

status = result["status"]
output = result["output"]
```

Voorbeeld voor SQLite:

```python
save_deployment_log(
    user_id=user_id,
    setup_id=setup_id,
    status=result["status"],
    output=result["output"]
)
```

De tabel `deployment_logs` verwacht dezelfde waarden.
Daarom heeft `status` in SQLite alleen deze toegelaten waarden:

```text
success
failed
```

Zo spreken Ansible, Flask en SQLite dezelfde taal.

## 3. Flask-template data

Lina werkt in:

```text
app.py
templates/login.html
templates/dashboard.html
```

Het dashboard verwacht later deze data:

```python
user = {
    "id": 1,
    "username": "docent",
    "role": "teacher"
}

network_setups = [
    {
        "id": 1,
        "name": "Basisopstelling",
        "description": "1 router, 1 switch, HTTP, HTTPS en FTP"
    }
]

last_log = {
    "status": "success",
    "output": "Ansible-output...",
    "timestamp": "2026-05-07 10:00:00"
}
```

Als er nog geen log is:

```python
last_log = None
```

## 4. Ansible-structuur

Bart werkt in:

```text
ansible/inventory.ini
ansible/playbooks/setup1/info.yml
ansible/playbooks/setup1/router.yml
ansible/playbooks/setup1/switch.yml
ansible/playbooks/setup1/servers.yml
```

Vaste afspraak:

| Bestand | Doel |
| --- | --- |
| `inventory.ini` | Bevat groepen `routers` en `switches`. |
| `setup1/info.yml` | Bevat toonbare setupinformatie en later configureerbare basiswaarden. |
| `setup1/router.yml` | Bevat routertaken voor basisopstelling 1. |
| `setup1/switch.yml` | Bevat switchtaken voor basisopstelling 1. |
| `setup1/servers.yml` | Bevat server/Docker-gerelateerde taken of demo-output voor basisopstelling 1. |

Groepen in inventory:

```ini
[routers]
r1 ansible_host=...

[switches]
sw1 ansible_host=...
```

Voor de MVP gebruiken we minimaal:

- 1 router;
- 1 switch;
- 1 setup-id uit SQLite.

### Setupdata

Voor Sprint 2 spreken we af dat `info.yml` de centrale plaats wordt voor:

- de naam en beschrijving van de opstelling;
- de apparaten die op het dashboard getoond worden;
- basiswaarden zoals hostnames, VLANs, interfacenamen en IP-adressen.

`info.yml` bevat daarom twee soorten informatie:

| Onderdeel | Doel |
| --- | --- |
| `devices` | Menselijke informatie voor het dashboard. |
| `variables` | Technische waarden die de playbooks gebruiken. |

Voorbeelden van waarden in `variables`:

- routerhostname;
- routerinterface;
- router-IP en subnetmasker;
- OSPF-waarden;
- switchhostname;
- VLAN-nummers en VLAN-namen;
- accesspoort en trunkpoort;
- serverpoorten en testgegevens.

De router- en switchplaybooks halen hun waarden zoveel mogelijk uit `info.yml`.
Daardoor blijft de informatie op het dashboard afgestemd op wat Ansible echt configureert.

Belangrijk:

- `info.yml` is geen databasevervanger;
- SQLite bepaalt welke setup bestaat;
- `playbook_data` in SQLite verwijst naar de juiste setupmap;
- `info.yml` beschrijft wat in die setup zit.

### Backups

Voor Sprint 2 voorzien we eenvoudige configuratiebackups.

Doel:

```text
running-config van router/switch ophalen en bewaren in backups/
```

De map `backups/` staat op de hostmachine en wordt via Docker Compose gekoppeld aan:

```text
/app/backups
```

Daardoor kunnen de Ansible-playbooks vanuit de Flask-container backupbestanden schrijven,
terwijl die bestanden ook zichtbaar blijven in de projectmap op de pc.

Bestandsnaam:

```text
<toestel>-<docent>-<datumtijd>-running-config.txt
```

Voorbeeld:

```text
r1-docent-20260519-214122-running-config.txt
sw1-docent-20260519-214218-running-config.txt
```

De datum/tijd in de bestandsnaam gebruikt Belgische tijd:

```text
Europe/Brussels
```

De docentnaam komt vanuit Flask.
Flask geeft de aangemelde username mee aan `run_setup`.
`ansible_tools.py` geeft die waarde aan Ansible door als extra variabele `logged_user`.

Dit is bewust beperkt:

- wel configuratie exporteren;
- geen volledig restoreplatform;
- geen complexe versiebeheerlogica in de webinterface.

## 5. Docker-structuur

Bart werkt in:

```text
Dockerfile
docker-compose.yml
servers/http/
servers/https/
servers/ftp/
```

Vaste services in Docker Compose:

| Service | Poort | Doel |
| --- | --- | --- |
| `flask` | intern `5000`, extern `5000` | Centrale Flask-applicatie. |
| `http` | `80` | HTTP-servercontainer. |
| `https` | `443` | HTTPS-servercontainer. |
| `ftp` | `20/21` | FTP-servercontainer. |

Elke image is gebaseerd op Alpine Linux.

### Docker CLI in de Flask-container

De Flask-container bevat naast Python en Ansible ook Docker CLI en Docker Compose CLI.

Reden:

- Flask start via `run_setup(setup_id, logged_user=session["username"])` de Ansible-flow;
- de Ansible-flow voert ook `servers.yml` uit;
- `servers.yml` moet in Sprint 2 servercontainers kunnen starten of controleren;
- daarvoor moet de Flask-container het commando `docker compose` kunnen gebruiken.

Belangrijk:

- Docker Compose blijft verantwoordelijk voor de servercontainers;
- de knop **Start configuratie** start de configuratieflow van de basisopstelling;
- binnen die flow kan het serverplaybook HTTP, HTTPS en FTP starten/controleren;
- dit is een labo/MVP-keuze en geen productie-security aanpak.

## 6. Belangrijkste regel

Als iemand een vaste naam, functie, tabel, veld of returnformaat wil wijzigen, moet dat eerst met het team besproken worden.

Anders breekt het werk van iemand anders.
