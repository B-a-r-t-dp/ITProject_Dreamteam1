# Opstartdocument

## 1. Opdracht

We maken een centrale beheeromgeving waarmee een docent een netwerkopstelling kan kiezen.

Na de keuze start de Flask-applicatie een Ansible-flow. Die flow is bedoeld om netwerkapparaten en servercontainers te configureren.

De opdracht combineert:

- Flask;
- SQLite;
- Ansible;
- Docker;
- Alpine Linux images;
- Debian Docker-host;
- router- en switchconfiguratie;
- HTTP-, HTTPS- en FTP-servercontainers.

## 2. Haalbare MVP

We bouwen niet meteen het volledige ideale platform. We bouwen eerst een kleine versie die de kern toont.

Onze MVP:

1. docent kan aanmelden;
2. docent ziet een dashboard;
3. dashboard toont 1 netwerkopstelling;
4. docent kan een configuratie starten;
5. Flask start een Ansible-flow;
6. status/output wordt opgeslagen in SQLite;
7. project bevat basis voor 1 router, 1 switch, HTTP, HTTPS en FTP;
8. project draait via Docker Compose met eigen Alpine-images.

## 3. Grenzen van de MVP

We houden het bewust klein:

- 1 docentaccount;
- 1 netwerkopstelling;
- eenvoudige templates;
- eenvoudige SQLite-tabellen;
- eenvoudige Ansible-playbooks;
- geen adminpagina;
- geen realtime output;
- geen CI/CD;
- geen volledig productiebeveiligd platform.

De volledige motivatie staat in:

```text
docs/mvp-afbakening.md
```

De planning over 4 sprints staat in:

```text
docs/scope-4-sprints.md
```

## 4. Taakverdeling

| Deel | Persoon | Verantwoordelijkheid | Bestandseigenaar van |
| --- | --- | --- | --- |
| Flask / frontend | Lina | Login, dashboard, knop, output tonen. | `app.py`, `templates/login.html`, `templates/dashboard.html`, `static/` |
| SQLite / backend | Joost | Database, users, network_setups, deployment_logs. | `database/schema.sql`, `modules/database_tools.py`, `data/` |
| Ansible / Docker / netwerk | Bart | Playbooks, inventory, Dockerfiles, Compose, router/switch/serverbasis. | `modules/ansible_tools.py`, `ansible/inventory.ini`, `ansible/playbooks/`, `Dockerfile`, `docker-compose.yml`, `servers/` |

Bestandseigenaar betekent:

- die persoon weet wat er in dat bestand staat;
- die persoon kan uitleggen waarom het nodig is;
- die persoon controleert dat wijzigingen in dat bestand blijven werken;
- andere teamleden mogen helpen, maar spreken af met de eigenaar.

## 5. Samenwerking tussen de delen

Iedereen kan aan zijn eigen deel werken zonder te wachten op de anderen.

We spreken vaste koppelpunten af:

| Koppelpunt | Afspraak |
| --- | --- |
| Netwerkopstelling | SQLite bevat minstens 1 setup met naam, beschrijving en playbook-info. |
| Ansible-resultaat | Ansible-functie geeft altijd `status` en `output` terug. |
| Dashboard | Frontend toont wat backend teruggeeft, zonder zelf Ansible-logica te kennen. |
| Logs | Elke uitvoering komt in `deployment_logs`. |

De volledige technische koppelafspraken staan in:

```text
docs/koppelafspraken.md
```

Belangrijk: vaste functienamen, tabelnamen, veldnamen en outputformaten mogen niet zomaar gewijzigd worden. Anders werken de delen niet meer samen.

## 6. Werkende versie na elke sprint

Na elke sprint moet het project nog kunnen starten.

Regels:

- geen half kapotte code op `main`;
- onafgewerkte functies blijven op een branch;
- bestaande werking wordt niet bewust gebroken;
- sprintreview vermeldt wat werkt en wat nog niet werkt.
