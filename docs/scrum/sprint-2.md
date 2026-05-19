# Sprint 2 - Integratie en uitbreiding van de basisopstelling

## Doel

In Sprint 1 hebben we de basis klaargezet: login, dashboard, SQLite, Ansible-helper, Dockerbestanden, playbooks en de eerste `setup1`-structuur.

Sprint 2 gebruiken we om van die basis een werkende en beter verdedigbare MVP te maken.

Het doel van Sprint 2 is:

```text
Een docent logt in
-> kiest de basisopstelling
-> klikt op Start configuratie
-> Flask start Ansible
-> Ansible voert de router-, switch- en servertaken uit
-> output/status wordt opgeslagen in SQLite
-> het dashboard toont wat er gebeurd is
```


## Gekozen backlogtaken


| PB-ID | Taak | Wat betekent dit concreet? | Eigenaar | Bestand(en) | Status |
| --- | --- | --- | --- | --- | --- |
| PB-37 | Startknop op het dashboard laten werken | Als de docent op de knop klikt, moet er een POST naar `/deploy` gebeuren met de juiste setup-id. | Lina | `templates/dashboard.html`, `app.py` | To do |
| PB-38 | Flask de Ansible-helper laten starten | `app.py` mag zelf geen Ansible-code bevatten. Lina koppelt de route aan `run_setup(setup_id)`. Bart zorgt dat de helper klaarstaat. | Lina | `app.py`, `modules/ansible_tools.py` | To do |
| PB-39 | Resultaat van Ansible opslaan in SQLite | Joost zorgt dat `success` of `failed` plus de tekstoutput correct in `deployment_logs` terechtkomt. | Joost | `modules/database_tools.py`, `app.py` | To do |
| PB-40 | Laatste run tonen op het dashboard | Lina toont de laatste status/output op het dashboard met de data die uit `database_tools.py` komt. | Lina | `app.py`, `templates/dashboard.html` | To do |
| PB-66 | Logs per docent controleren | Joost controleert of logs gekoppeld zijn aan de aangemelde docent. Hiervoor voorzien we ook een tweede testdocent. Dit is belangrijk om later te weten wie wat gestart heeft. | Joost | `modules/database_tools.py`, `app.py` | To do |
| PB-41 | HTTP-container starten en testen | Controleren of de gewone webserver via Docker Compose kan starten en bereikbaar is op poort 80. | Bart | `servers/http/`, `docker-compose.yml`, `ansible/playbooks/setup1/servers.yml` | Done |
| PB-42 | HTTPS-container testen | Controleren of de beveiligde webserver start en bereikbaar is op poort 443. | Bart | `servers/https/`, `docker-compose.yml`, `ansible/playbooks/setup1/servers.yml` | Done |
| PB-43 | Self-signed certificaat voorzien voor HTTPS | Voor de MVP mag dit een self-signed certificaat zijn. | Bart | `servers/https/Dockerfile`, `servers/https/default.conf` | Done  |
| PB-44 | FTP-container testen | Controleren of de FTP-service start en bereikbaar is op poort 20/21 | Bart | `servers/ftp/`, `docker-compose.yml` | Done |
| PB-45 | FTP-gebruiker en testbestand voorzien | Er moet een eenvoudige FTP-gebruiker en testbestand zijn, zodat we kunnen aantonen dat FTP werkt. | Bart | `servers/ftp/Dockerfile`, `servers/ftp/vsftpd.conf` | Done |
| PB-65 | Serverplaybook nuttiger maken | Het serverplaybook mag niet alleen tekst tonen, maar ook eenvoudige checks uitvoeren of duidelijk tonen wat getest wordt. | Bart | `ansible/playbooks/setup1/servers.yml`, `docker-compose.yml` | Done |
| PB-46 | Routerplaybook testen in EVE-NG | Controleren of Ansible de router kan bereiken en de basisconfiguratie kan uitvoeren. | Bart | `ansible/playbooks/setup1/router.yml`, `ansible/inventory.ini` | Done |
| PB-47 | Switchplaybook testen in EVE-NG | Controleren of Ansible de switch kan bereiken en VLANs/poorten kan configureren. | Bart | `ansible/playbooks/setup1/switch.yml`, `ansible/inventory.ini` | Done |
| PB-48 | Docker Compose opnieuw bouwen en starten | Controleren of de Flask-container en servercontainers opnieuw correct bouwen en starten. | Bart | `docker-compose.yml`, `Dockerfile`, `servers/` | Done |
| PB-63 | IP-adressering van de basisopstelling uitschrijven | We documenteren welke IP's gebruikt worden voor management, routerinterface, VLANs en servers. | Bart | `docs/`, `ansible/inventory.ini`, `ansible/playbooks/setup1/info.yml` | Done |
| PB-69 | `info.yml` uitbreiden met variabelen | `info.yml` bevat niet alleen tekst voor het dashboard, maar ook waarden zoals hostname, interface, VLAN en IP. | Bart | `ansible/playbooks/setup1/info.yml` |Done |
| PB-70 | Routerplaybook laten werken met variabelen uit de setup | De routerconfiguratie wordt minder hardcoded. Waarden zoals hostname en interface-IP komen uit setupdata. | Bart | `ansible/playbooks/setup1/router.yml`, `ansible/playbooks/setup1/info.yml` | Done |
| PB-71 | Switchplaybook laten werken met variabelen uit de setup | VLAN-nummers, VLAN-namen en poorten worden duidelijker gekoppeld aan de setupdata. | Bart | `ansible/playbooks/setup1/switch.yml`, `ansible/playbooks/setup1/info.yml` | Done |
| PB-75 | Op dashboard tonen welke variabelen gebruikt worden | Lina toont de waarden uit `info.yml` duidelijk op het dashboard. Bart zorgt dat de inhoud van `info.yml` klopt. | Lina | `templates/dashboard.html`, `modules/database_tools.py`, `ansible/playbooks/setup1/info.yml` | To do |
| PB-72 | Backupmap gebruiken | We gebruiken de map `backups/` om configuratiebestanden uit router en switch te bewaren. | Bart | `backups/`, `docker-compose.yml` | Done |
| PB-73 | Routerconfiguratie als backup bewaren | Ansible haalt de running-config van de router op en bewaart die als tekstbestand. | Bart | `ansible/playbooks/setup1/router.yml`, `backups/` | Done |
| PB-74 | Switchconfiguratie als backup bewaren | Ansible haalt de running-config van de switch op en bewaart die als tekstbestand. | Bart | `ansible/playbooks/setup1/switch.yml`, `backups/` | Done |
| PB-60 | Ansible-output leesbaarder maken | Lina zorgt dat de output op het dashboard overzichtelijker wordt weergegeven. Bart blijft verantwoordelijk voor de ruwe Ansible-output. | Lina | `templates/dashboard.html`, `static/style.css` | To do |
| PB-61 | Fouten duidelijker tonen | Lina toont fouten duidelijker in de webinterface. De technische fouttekst blijft uit `modules/ansible_tools.py` komen. | Lina | `app.py`, `templates/dashboard.html` | To do |
| PB-64 | Netwerkschema of podschema maken | We tekenen of documenteren hoe router, switch, managementnetwerk en containers samenhangen. | Lina | `docs/` | To do |
| PB-76 | Koppelafspraken bijwerken | Als we `info.yml`, backups of outputformaat aanpassen, moet dit ook in de teamafspraken staan. | Team | `docs/koppelafspraken.md`, `docs/mvp-afbakening.md` | Done |

### Doorschuifbare taken

Deze taken nemen we al op in Sprint 2 omdat ze nuttig zijn voor de MVP. Als de basisflow, Docker, Ansible en logging nog te veel tijd vragen, mogen deze taken zonder probleem doorschuiven naar Sprint 3.

| PB-77 | Klein formulier voorzien voor setupwaarden | Lina maakt een eenvoudig formulier of scherm waar setupwaarden zichtbaar en eventueel aanpasbaar zijn. | Lina | `templates/dashboard.html`, `app.py` | To do |
| PB-78 | Aangepaste waarden doorgeven aan Ansible | Joost voorziet hoe aangepaste waarden tijdelijk of via database/helper worden doorgegeven aan de configuratieflow. | Joost | `modules/database_tools.py`, `app.py` | To do |
| PB-79 | Invoer controleren | Joost controleert basisfouten, bijvoorbeeld lege hostnames, verkeerde VLAN-nummers of ongeldige IP-adressen. | Joost | `modules/database_tools.py`, `app.py` | To do |


## Daily stand-ups

| Moment | Tijdstip | Medium | Korte notities |
| --- | --- | --- | --- |
| Dinsdag daily 1 | 20:00 | MS Teams |  |
| Woensdag daily 2 | 20:00 | MS Teams |  |
| Donderdag daily 3 | 20:00 | MS Teams |  |
| Beslissen op donderdag  daily 4 | 20:00 | MS Teams |  |

Tijdens elke daily bespreken we:

- wat heb ik gedaan?
- wat ga ik nu doen?
- waar zit ik vast?

## Werkende sprintversie

Op het einde van Sprint 2 moet dit werken of duidelijk aantoonbaar zijn:

- een docent kan aanmelden;
- dashboard toont de basisopstelling;
- startknop start de configuratieflow;
- Flask roept de Ansible-helper aan;
- router-, switch- en serverplaybooks worden uitgevoerd of duidelijk getest;
- output/status wordt opgeslagen in SQLite;
- laatste status/output verschijnt op het dashboard;
- HTTP, HTTPS en FTP zijn getest;
- `setup1/info.yml` beschrijft de basisopstelling en bevat basiswaarden;
- de gebruikte setupwaarden worden zichtbaar gemaakt;
- running-config backups van router en switch zijn voorzien of technisch verantwoord;
- IP-adressering en netwerkschema zijn voorbereid;
- fouten en output zijn begrijpelijk genoeg voor de demo.
