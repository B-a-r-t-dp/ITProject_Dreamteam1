# Sprint 1 - Basis en taakverdeling

## Doel

De projectbasis staat klaar en iedereen weet welk deel en welke bestanden van hem/haar zijn.

## Gekozen backlogtaken

| PB-ID | Taak | Eigenaar | Bestand(en) | Status |
| --- | --- | --- | --- | --- |
| PB-01 | Projectstructuur controleren | Team | `README.md`, alle hoofdmappen | Done |
| PB-02 | Opstartdocument bespreken | Team | `docs/opstartdocument.md` | Done |
| PB-03 | MVP-afbakening bespreken | Team | `docs/mvp-afbakening.md` | Done |
| PB-04 | Scope over 4 sprints bespreken | Team | `docs/scope-4-sprints.md` | Done |
| PB-05 | Taakverdeling en bestandseigenaars bevestigen | Team | `README.md`, `docs/opstartdocument.md` | Done |
| PB-06 | AI-logboek, changelog en koppelafspraken uitleggen | Team | `docs/personen/*/ai-logboek.md`, `docs/personen/*/changelog.md`, `docs/koppelafspraken.md` | Done |
| PB-07 | Loginpagina als template klaarzetten | Lina | `templates/login.html` | Done |
| PB-08 | Dashboardpagina als template klaarzetten | Lina | `templates/dashboard.html` | Done |
| PB-09 | Plaats voorzien voor netwerkopstellingen op dashboard | Lina | `templates/dashboard.html` | Done |
| PB-10 | Plaats voorzien voor status/output op dashboard | Lina | `templates/dashboard.html` | Done |
| PB-11 | SQLite-schema voor `users` uitwerken | Joost | `database/schema.sql` | Done |
| PB-12 | SQLite-schema voor `network_setups` uitwerken | Joost | `database/schema.sql` | Done |
| PB-13 | SQLite-schema voor `deployment_logs` uitwerken | Joost | `database/schema.sql` | Done |
| PB-14 | Relaties tussen tabellen voorbereiden | Joost | `database/schema.sql` | Done |
| PB-15 | Ansible-inventory invullen met router en switch | Bart | `ansible/inventory.ini` | Done |
| PB-16 | Routerplaybook als basis voorbereiden | Bart | `ansible/playbooks/setup1/router.yml` | Done |
| PB-17 | Switchplaybook als basis voorbereiden | Bart | `ansible/playbooks/setup1/switch.yml` | Done |
| PB-18 | Serverplaybook als basis voorbereiden | Bart | `ansible/playbooks/setup1/servers.yml` | Done |
| PB-19 | Flask Dockerfile controleren | Bart | `Dockerfile` | Done |
| PB-20 | Docker Compose controleren | Bart | `docker-compose.yml` | Done |
| PB-21 | HTTP Dockerfile controleren | Bart | `servers/http/Dockerfile`, `servers/http/default.conf`, `servers/http/index.html` | Done |
| PB-22 | HTTPS Dockerfile controleren | Bart | `servers/https/Dockerfile`, `servers/https/default.conf`, `servers/https/index.html` | Done |
| PB-23 | FTP Dockerfile controleren | Bart | `servers/ftp/Dockerfile`, `servers/ftp/vsftpd.conf` | Done |
| PB-24 | SQLite-database initialiseren vanuit schema | Joost | `modules/database_tools.py`, `database/schema.sql`, `data/` | Done |
| PB-25 | Testdocent aanmaken | Joost | `modules/database_tools.py` | Done |
| PB-26 | Password hashing toepassen voor testdocent | Joost | `modules/database_tools.py`, `requirements.txt` | Done |
| PB-27 | Minstens 1 netwerkopstelling opslaan in SQLite | Joost | `modules/database_tools.py`, `database/schema.sql` | Done |
| PB-28 | Functie maken om users te controleren | Joost | `modules/database_tools.py` | Done |
| PB-29 | Functie maken om network_setups op te halen | Joost | `modules/database_tools.py` | Done |
| PB-30 | Functie maken om deployment_logs op te slaan | Joost | `modules/database_tools.py` | Done |
| PB-31 | Loginroute koppelen aan SQLite | Lina + Joost | `app.py`, `modules/database_tools.py`, `templates/login.html` | Done |
| PB-32 | Logout voorzien | Lina | `app.py`, `templates/dashboard.html` | Done |
| PB-33 | Dashboard beschermen achter login | Lina | `app.py` | Done |
| PB-34 | Netwerkopstelling tonen op dashboard | Lina + Joost | `app.py`, `templates/dashboard.html`, `modules/database_tools.py` | Done |
| PB-35 | Ansible-helper voorbereiden met `status` en `output` | Bart | `modules/ansible_tools.py` | Done |
| PB-36 | Afspraak maken over outputformaat tussen Ansible, Flask en SQLite | Team | `modules/ansible_tools.py`, `modules/database_tools.py`, `app.py` | Done |
| PB-67 | Playbooks groeperen per netwerkopstelling in `setup1` | Bart | `ansible/playbooks/setup1/` | Done |
| PB-68 | Extra setupinformatie tonen op dashboard vanuit `setup1/info.yml` | Lina + Bart | `ansible/playbooks/setup1/info.yml`, `templates/dashboard.html`, `modules/database_tools.py` | Done |



## Daily Stand-ups

We plannen ongeveer 4 korte meetings per werkweek via MS Teams. Een daily duurt ongeveer 10 tot 15 minuten.

**12/05 Dinsdag daily 1 |  20:00 | MS Teams |**

**13/05 Woensdag daily 2 | 20:00 | MS Teams - bericht |**

**15/05 Vrijdag daily 3 | 19:00 | MS Teams |**

**16/05 Zaterdag daily 4 | 13:00 | MS Teams |**


**Tijdens elke daily bespreken we:**

- Wat heb ik gedaan?
- Wat ga ik nu doen?
- Waar zit ik vast?



## Werkende sprintversie

Op het einde moet dit werken of aanwezig zijn:

- Flask start;
- login- en dashboardpagina bestaan;
- SQLite-schema is voorbereid;
- Ansible-inventory en playbooks bestaan;
- Docker Compose-bestand bestaat;
- iedereen weet wat zijn/haar bestanden zijn.
- docent kan aanmelden;
- dashboard is alleen bereikbaar na login;
- minstens 1 netwerkopstelling komt uit SQLite;
- databasefuncties bestaan;
- Ansible-helper heeft een vaste returnstructuur.
- playbooks zijn gegroepeerd onder `ansible/playbooks/setup1/`;
- dashboard toont extra informatie over de basisopstelling vanuit `setup1/info.yml`.


## Review

- Wat is klaar?
- Wat is nog placeholder?
- Wat blokkeert?
- Kan een docent inloggen?
- Komt data uit SQLite?
- Zijn de koppelingen tussen Lina, Joost en Bart duidelijk?
