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
| PB-37 | Startknop op het dashboard laten werken | Als de docent op de knop klikt, moet er een POST naar `/deploy` gebeuren met de juiste setup-id. | Lina | `templates/dashboard.html`, `app.py` | done |
| PB-38 | Flask de Ansible-helper laten starten | `app.py` mag zelf geen Ansible-code bevatten. Lina koppelt de route aan `run_setup(setup_id)`. Bart zorgt dat de helper klaarstaat. | Lina | `app.py`, `modules/ansible_tools.py` | done |
| PB-39 | Resultaat van Ansible opslaan in SQLite | Joost zorgt dat `success` of `failed` plus de tekstoutput correct in `deployment_logs` terechtkomt. | Joost | `modules/database_tools.py`, `app.py` | Done |
| PB-40 | Laatste run tonen op het dashboard | Lina toont de laatste status/output op het dashboard met de data die uit `database_tools.py` komt. | Lina | `app.py`, `templates/dashboard.html` | Done |
| PB-66 | Logs per docent controleren | Joost controleert of logs gekoppeld zijn aan de aangemelde docent. Hiervoor voorzien we ook een tweede testdocent. Dit is belangrijk om later te weten wie wat gestart heeft. | Joost | `modules/database_tools.py`, `app.py` | Done |
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
| PB-60 | Ansible-output leesbaarder maken | Lina zorgt dat de output op het dashboard overzichtelijker wordt weergegeven. Bart blijft verantwoordelijk voor de ruwe Ansible-output. | Lina | `templates/dashboard.html`, `static/style.css` | Done |
| PB-61 | Fouten duidelijker tonen | Lina toont fouten duidelijker in de webinterface. De technische fouttekst blijft uit `modules/ansible_tools.py` komen. | Lina | `app.py`, `templates/dashboard.html` | Done |
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
| 19/05 Dinsdag daily 1 | 20:00 | MS Teams | Sprint 2 opgestart. We hebben afgesproken dat de focus eerst ligt op de volledige basisflow: knop op dashboard, Ansible starten, output opslaan en servercontainers testen. |
| 20/05 Woensdag daily 2 | 20:00 | MS Teams | We hebben verder getest met Docker, HTTP/HTTPS/FTP en EVE-NG. De meeste technische onderdelen werkten, maar FTP en de leesbaarheid van de output moesten nog duidelijker. |
| 21/05 Donderdag daily 3 | 20:00 | MS Teams | We hebben de router- en switchplaybooks verder gevalideerd en backups getest. Ook is beslist om de setupwaarden via `info.yml` centraal te houden. |
| 22/05 Vrijdag daily 4 | 20:00 | MS Teams | Sprint 2 is nagekeken. De basis-MVP hangt goed samen. De taken rond aanpasbare setupwaarden schuiven we bewust door naar Sprint 3. |

Tijdens elke daily bespreken we:

- wat heb ik gedaan?
- wat ga ik nu doen?
- waar zit ik vast?

**19/05 Dinsdag daily 1 | 20:00 | MS Teams |**
 
- Bart  
Ik heb vooral gekeken naar mijn Sprint 2-taken rond Docker, Ansible en de servercontainers. Daarbij hebben we ook bekeken dat de Docker-host een Debian-machine moet zijn waarop Docker Engine geïnstalleerd is en waarop Docker Compose gebruikt kan worden om de containers samen te starten. HTTP werkte al apart, maar we wilden dat de knop Start configuratie uiteindelijk de volledige basisopstelling start. Mijn volgende stap is het serverplaybook nuttiger maken, zodat HTTP, HTTPS en FTP niet alleen beschreven worden maar ook echt gestart en gecontroleerd worden. Waar ik nog rekening mee moet houden, is dat Docker Compose vanuit de Flask-container moet kunnen werken.
 
- Lina  
Lina heeft gekeken naar de startknop op het dashboard en hoe die naar `/deploy` moet posten met de juiste setup-id. De volgende stap is zorgen dat het dashboard de status en output duidelijk toont na een configuratierun. Daarbij moet ook duidelijk worden welke setup gestart wordt op de Docker-host. Ze moest nog afstemmen met Bart en Joost welke data exact uit Ansible en SQLite komt.
 
- Joost  
Joost heeft verder gekeken naar de databasekant. De deployment logs moeten gekoppeld blijven aan de juiste docent en setup. Daarbij is het ook belangrijk dat de juiste configuratierun op de Docker-host later correct gelogd wordt. De volgende stap is controleren of `success` en `failed` correct opgeslagen worden. Er moest nog extra getest worden met meerdere docenten zodat we zeker weten dat logs per gebruiker kloppen.
 
**20/05 Woensdag daily 2 | 20:00 | MS Teams |**
 
- Bart  
Ik heb de HTTP-, HTTPS- en FTP-container getest via Docker Compose op de Docker-host. De Docker-host is voorzien als Debian-machine waarop Docker Engine geïnstalleerd is. HTTP en HTTPS werkten vrij snel, maar FTP vroeg extra controle omdat poort 21 alleen niet genoeg is om te bewijzen dat FTP echt bruikbaar is. Mijn volgende stap is de FTP-login en het testbestand automatisch laten controleren in `servers.yml`. Waar ik nog tegenaan liep, was het verschil tussen poort open en effectief kunnen aanmelden/bestanden lezen.
 
- Lina  
Lina heeft verder gewerkt aan het dashboard. De setupinformatie uit `info.yml` wordt zichtbaar gemaakt zodat de frontend niet alles hardcoded moet tonen. De volgende stap is de output op het dashboard duidelijker maken. Daarbij moet de gebruiker kunnen zien of de configuratie op de Docker-host correct gestart is. Het was nog wat zoeken hoe veel technische output nuttig is voor een docent.
 
- Joost  
Joost heeft nagekeken of logs per docent goed opgehaald kunnen worden. De database bevat nu ook een tweede testdocent, zodat we kunnen testen dat een gebruiker alleen zijn eigen laatste configuratie ziet. Daarbij moet de logging ook bruikbaar blijven wanneer de containers via Docker Compose op de Debian Docker-host gestart worden. De volgende stap is samen controleren of de Flask-route de juiste `user_id` doorgeeft.
 
**21/05 Donderdag daily 3 | 20:00 | MS Teams |**
 
- Bart  
Ik heb de router- en switchplaybooks getest in EVE-NG. De router configureert hostname, labinterface, IP-adres en OSPF. De switch maakt VLAN 10 en VLAN 20 aan en zet de access- en trunkpoort goed. Daarnaast blijft het belangrijk dat de servercontainers op de Docker-host draaien en dat het netwerk tussen de containers correct geconfigureerd is. We hebben ook gemerkt dat oude configuratie op switchpoorten problemen kan geven, dus de poorten worden eerst gereset. Mijn volgende stap is backups voorzien van de running-configs.
 
- Lina  
Lina heeft gekeken naar hoe de laatste run duidelijker op het dashboard kan komen. De status wordt zichtbaar en de output staat in een aparte box. De volgende stap is fouten duidelijker tonen, zodat je niet heel de ruwe Ansible-output moet lezen om te weten wat er misliep. Dit is ook nuttig om te tonen of een probleem uit Ansible, Docker Compose of de Docker-host komt.
 
- Joost  
Joost heeft verder afgestemd met de databasefuncties. De logs worden opgeslagen met setup-id, user-id, status en output. De volgende stap is controleren dat de database niet te veel logica in `app.py` duwt. Er was geen grote blokkade meer, vooral nog testen met echte output van Ansible en Docker Compose, zodat geslaagde en mislukte configuraties correct worden opgeslagen.
 
**22/05 Vrijdag daily 4 | 20:00 | MS Teams |**
 
- Bart  
Ik heb de backupflow afgewerkt. Router en switch bewaren hun running-config in `backups/` met toestelnaam, docentnaam en timestamp. Daarna hebben we ook de Ansible-output leesbaarder gemaakt met een samenvatting en een uitklapbare technische output. FTP is nog verbeterd met passive poorten zodat WinSCP/FileZilla beter werken. De Docker-host blijft hierbij de Debian-machine waarop de containers draaien via Docker Compose. Mijn Sprint 2-taken zijn daarmee klaar. Voor Sprint 3 wil ik mee nadenken over een tweede opstelling en inventory per setup.
 
- Lina  
Lina heeft het dashboard verder verbeterd. De gebruiker ziet nu duidelijker of de laatste configuratie gelukt of mislukt is. De samenvatting staat direct zichtbaar en de technische output kan opengeklapt worden. Daardoor kan de docent beter volgen wat er op de achtergrond gebeurt, zonder alle ruwe output van Ansible of Docker Compose te moeten lezen. De taken rond een formulier om setupwaarden aan te passen schuiven door naar Sprint 3, omdat dat een aparte uitbreiding is.
 
- Joost  
Joost heeft gecontroleerd of de logging en databaseflow blijven kloppen met de nieuwe output. De basis werkt: logs worden opgeslagen en per docent opgehaald. Daarbij is ook rekening gehouden met het feit dat de containers op een Debian Docker-host draaien en dat de resultaten van die configuratieruns correct in de database moeten terechtkomen. Voor Sprint 3 neemt Joost vooral de validatie van aangepaste setupwaarden mee, zodat verkeerde IP-adressen of VLAN-nummers niet zomaar doorgestuurd worden.
 

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
- `setup1/info.yml` beschrijft de basisopstelling en bevat variabelen;
- de gebruikte setupwaarden worden zichtbaar gemaakt;
- running-config backups van router en switch zijn voorzien of technisch verantwoord;
- IP-adressering en netwerkschema zijn voorbereid => documentatie;
- fouten en output zijn begrijpelijk genoeg voor de demo.
