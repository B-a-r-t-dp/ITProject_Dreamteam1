# ITProject MVP

```text
Geautomatiseerde netwerk- en serverconfiguratie via Flask, Ansible en Docker
```

We bouwen bewust een haalbare MVP:

- 1 docent kan aanmelden;
- 1 netwerkopstelling kan geselecteerd worden;
- Flask start een Ansible-flow;
- output/status wordt opgeslagen in SQLite;
- Ansible richt zich op 1 router, 1 switch, HTTP, HTTPS en FTP;
- alles draait via eigen Alpine Docker-images op een Debian Docker-host.

## Belangrijkste documenten

| Document | Doel |
| --- | --- |
| [Opstartdocument](docs/opstartdocument.md) | Uitleg over opdracht, MVP, taakverdeling en werkwijze. |
| [MVP-afbakening](docs/mvp-afbakening.md) | Wat we bouwen, beperkt bouwen en bewust niet bouwen. |
| [Koppelafspraken](docs/koppelafspraken.md) | Vaste functies, tabellen en outputformaten zodat de delen samenwerken. |

##  Scrum methode

| Document | Doel |
| --- | --- |
| [Scope over 4 sprints](docs/scrum/scope-4-sprints.md) | voorbeeld planning om de MVP in 4 sprints af te werken. |
| [Product backlog](docs/scrum/product-backlog.md) | backlog voor het project. |
| [Sprint 1](docs/scrum/sprint-1.md) | Basis en taakverdeling, Flask en SQLite. |

## Taakverdeling en bestandseigenaars

| Persoon | Deel | Verantwoordelijk voor deze bestanden/mappen |
| --- | --- | --- |
| Lina | Flask / frontend | `app.py`, `templates/login.html`, `templates/dashboard.html`, `static/` |
| Joost | SQLite / backend | `database/schema.sql`, `modules/database_tools.py`, `data/` |
| Bart | Ansible / Docker / netwerk | `modules/ansible_tools.py`, `ansible/inventory.ini`, `ansible/playbooks/`, `Dockerfile`, `docker-compose.yml`, `servers/http/`, `servers/https/`, `servers/ftp/` |

Iedereen werkt aan een eigen deel, maar spreekt vaste afspraken af voor hoe de delen samenkomen.

Belangrijk: we helpen elkaar indien nodig, maar de eigenaar blijft verantwoordelijk dat het bestand begrijpbaar, getest en gedocumenteerd is.

## Projectstructuur

```text
projectnew/
|-- app.py
|-- requirements.txt
|-- Dockerfile
|-- docker-compose.yml
|-- database/
|-- ansible/
|-- servers/
|-- modules/
|-- templates/
|-- static/
|-- data/
|-- backups/
|-- docs/
|-- README.md
```
