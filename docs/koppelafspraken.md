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

Deze functies moeten bestaan:

```python
init_database()
verify_user(username, password)
get_network_setups()
save_deployment_log(user_id, setup_id, status, output)
get_last_deployment_log()
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
        "description": "1 router, 1 switch, HTTP, HTTPS en FTP"
    }
]
```

### Bart - ansible_tools.py

Deze functie moet bestaan:

```python
run_setup(setup_id)
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

### Afspraak outputformaat Ansible -> Flask -> SQLite

`modules/ansible_tools.py` is verantwoordelijk voor het starten van de Ansible-flow.
Flask mag dus niet zelf rechtstreeks `ansible-playbook` starten.

Flask roept alleen deze functie aan:

```python
result = run_setup(setup_id)
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
result = run_setup(setup_id)

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
ansible/playbooks/router.yml
ansible/playbooks/switch.yml
ansible/playbooks/servers.yml
```

Vaste afspraak:

| Bestand | Doel |
| --- | --- |
| `inventory.ini` | Bevat groepen `routers` en `switches`. |
| `router.yml` | Bevat routertaken. |
| `switch.yml` | Bevat switchtaken. |
| `servers.yml` | Bevat server/Docker-gerelateerde taken of demo-output. |

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
| `flask` | `5000` | Centrale Flask-applicatie. |
| `http` | `80` | HTTP-servercontainer. |
| `https` | `443` | HTTPS-servercontainer. |
| `ftp` | `20/21` | FTP-servercontainer. |

Elke image is gebaseerd op Alpine Linux.

## 6. Belangrijkste regel

Als iemand een vaste naam, functie, tabel, veld of returnformaat wil wijzigen, moet dat eerst met het team besproken worden.

Anders breekt het werk van iemand anders.
