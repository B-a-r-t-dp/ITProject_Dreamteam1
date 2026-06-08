# Sprint 4 - Oplevering, documentatie en demo voorbereiden

## Doel

Sprint 4 gebruiken we om de afgewerkte MVP klaar te maken voor de evaluatie.

In deze sprint bouwen we geen nieuwe grote functionaliteiten meer. De applicatie wordt gezien als de afgewerkte MVP. We focussen dus op:

```text
documenteren, testen, demo voorbereiden en zorgen dat iedereen de code begrijpt.
```

Alleen als er tijdens het testen nog een kleine fout gevonden wordt die de demo blokkeert, mag er nog code aangepast worden. Grote refactors of nieuwe features horen niet meer in Sprint 4.


## Sprint 4 afspraken

- Geen nieuwe grote codeaanpassingen meer.
- Alleen kleine bugfixes als iets de demo of evaluatie blokkeert.
- Iedereen documenteert de bestanden waarvoor hij of zij verantwoordelijk is.
- Commentaar in code blijft kort, duidelijk en nuttig.
- Als code onnodig complex is, mag die eenvoudiger gemaakt worden, maar alleen als dit weinig risico geeft en de hele flow niet breekt.
- Het technisch document wordt afgewerkt volgens de vereisten van de opgave.
- De demo-flow wordt volledig getest.
- Iedereen moet zijn of haar code kunnen uitleggen tijdens de evaluatie.


## Gekozen taken sprint 4

| PB-ID | Taak | Wat betekent dit concreet? | Eigenaar | Bestand(en) | Status |
| --- | --- | --- | --- | --- | --- |
| PB-49 | Volledige demo-flow testen | We testen de demo alsof de docent meekijkt: login, setup kiezen, waarden aanpassen, configuratie starten, output bekijken, geschiedenis controleren en backups downloaden. | Team | volledige project | Done |
| PB-50 | Testen of `main` een werkende sprintversie bevat | We controleren of de gepushte versie opnieuw kan starten vanaf een propere checkout. | Team | GitHub, Docker Compose | Done |
| PB-51 | Docker Compose build/start documenteren | De stappen om Docker-images te bouwen en containers te starten worden duidelijk uitgelegd. | Bart | `Dockerfile`, `docker-compose.yml`, `servers/`, technisch document | Done |
| PB-52 | SQLite-tabellen en logs documenteren | De database, tabellen, gebruikers, setupdata en deployment logs worden duidelijk uitgelegd. | Joost | `database/schema.sql`, `modules/database_tools.py`, technisch document | Done |
| PB-53 | Flask-flow documenteren | De login, dashboardflow, routes, templates en frontendwerking worden duidelijk gedocumenteerd. | Lina | `app.py`, `templates/`, `static/`, technisch document | Done |
| PB-54 | Netwerk/Ansible-beperkingen documenteren | We leggen uit wat setup1 en setup2 configureren, welke basisconfiguratie nodig is en wat bewust beperkt blijft. | Bart | `ansible/playbooks/`, setupdocumentatie, technisch document | Done |
| PB-55 | MVP-afbakening finaliseren | We controleren of de MVP-afbakening overeenkomt met wat echt gebouwd is. | Team | `docs/mvp-afbakening.md`, technisch document | Done |
| PB-56 | Niet-afgewerkte onderdelen verantwoorden | Alles wat niet volledig uit de opgave gebouwd is, wordt eerlijk verantwoord als MVP-keuze. | Team | technisch document | Done |
| PB-57 | Presentatie/demo voorbereiden | We maken een vaste demo-volgorde zodat we tijdens de evaluatie niet moeten improviseren. | Team | demo-checklist, technisch document | Done |
| PB-58 | AI-logboeken en changelogs controleren | Iedereen controleert of zijn of haar AI-logboek en changelog volledig en verdedigbaar zijn. | Team | `docs/personen/` | Done |
| PB-96 | Code per eigenaar nalezen en kort documenteren | Iedereen leest zijn eigen bestanden na en voegt waar nodig korte commentaar toe zodat de code begrijpbaar is. | Team | projectbestanden per eigenaar | Done |
| PB-97 | Technisch document als einddocument afwerken | Het technische document wordt ingevuld volgens de opgave en samengebracht tot 1 verhaal. | Team | `technische-documentatie.docx` | Done |


## Status Sprint 4

Deze Sprint 4-onderdelen zijn afgerond:

- PB-49: de volledige demo-flow is getest met login, setupkeuze, configuratie, output, geschiedenis en backups.
- PB-50: de gepushte versie werd opnieuw opgehaald en gestart op de Debian Docker-host.
- PB-51: Docker Compose build/start is uitgewerkt in het technisch document.
- PB-52: SQLite-tabellen, users, setupdata en deployment logs zijn gedocumenteerd.
- PB-53: Flask-flow, routes, sessies, templates en dashboardwerking zijn gedocumenteerd.
- PB-54: Netwerk- en Ansible-beperkingen zijn uitgewerkt voor setup1 en setup2.
- PB-55: De MVP-afbakening is gecontroleerd tegenover wat effectief gebouwd werd.
- PB-56: Niet-afgewerkte of beperkte onderdelen zijn verantwoord als MVP-keuze.
- PB-57: De demo-flow is voorbereid zodat we tijdens de evaluatie niet moeten improviseren.
- PB-58: AI-logboeken en changelogs zijn nagekeken.
- PB-96: De code werd per eigenaar nagelezen en kort gedocumenteerd.
- PB-97: Het technisch document is afgewerkt als einddocument.


## Documentatieverdeling

We werken allemaal in dezelfde structuur van het technisch document. Zo blijft het einddocument 1 geheel.

### Bart

Bart werkt vooral aan infrastructuur, Ansible, Docker en de netwerkopstellingen.

Onderwerpen:

- architectuur van de technische opstelling;
- setup1 basisopstelling;
- setup2 podopstelling Brussel;
- Ansible-inventories;
- Ansible-playbooks;
- variabelen in `info.yml`;
- router- en switchconfiguratie;
- serverplaybook;
- Dockerfiles;
- `docker-compose.yml`;
- poorten, volumes en netwerken;
- backups van running-configs;
- beperkingen rond EVE-NG, SSH en basisconfiguratie.

### Joost

Joost werkt vooral aan de installatiehandleiding en database-uitleg.

Onderwerpen:

- installatie van Debian;
- installatie van Docker;
- installatie van Docker Compose;
- project ophalen op de Debian Docker-host;
- Docker-images builden;
- containers starten;
- SQLite initialiseren;
- database-tabellen uitleggen;
- deployment logs uitleggen;
- testgebruikers en password hashing uitleggen.

### Lina

Lina werkt vooral aan de diagrammen en de Flask-applicatie.

Onderwerpen:

- technisch diagram voor setup1 met interfaces;
- technisch diagram voor setup2 met interfaces;
- uitleg over login/logout;
- uitleg over dashboard;
- uitleg over beschikbare netwerkopstellingen;
- uitleg over status, output, geschiedenis en backups in de frontend;
- korte uitleg over templates en CSS.


## Technisch document - vaste structuur

Het technisch document volgt de vereisten uit de opgave.

### 1. Architectuur

In dit hoofdstuk komt het algemene verhaal:

- overzicht van de volledige opstelling;
- hoe Flask, SQLite, Ansible en Docker samenwerken;
- netwerkschema;
- Docker-containeroverzicht;
- IP-adresseringsschema;
- beschrijving van router, switch en servers.

### 2. Opstelling 1 - Basisopstelling

In dit hoofdstuk komt setup1:

- doel van setup1;
- technisch diagram met interfaces;
- IP-adressering;
- basisconfiguratie voor SSH;
- routerconfiguratie;
- switchconfiguratie;
- servercontainers;
- controlecommando's.

### 3. Opstelling 2 - Podopstelling Brussel

In dit hoofdstuk komt setup2:

- link met de labo-pod-opgave;
- waarom we 1 pod volledig uitwerken;
- technisch diagram met interfaces;
- IP-adressering;
- basisconfiguratie voor SSH;
- router-on-a-stick;
- VLANs;
- trunks;
- EtherChannel;
- classroom accesspoorten;
- controlecommando's.

### 4. Installatiehandleiding

In dit hoofdstuk komt de handleiding voor de Debian Docker-host:

- Debian installeren of voorbereiden;
- Docker installeren;
- Docker Compose installeren;
- project ophalen;
- Docker-images builden;
- containers starten;
- SQLite initialiseren;
- Flask-applicatie openen.

### 5. Flask-applicatie

In dit hoofdstuk komt de uitleg over de webapplicatie:

- gebruikte Python-packages;
- structuur van de applicatie;
- login/logout;
- dashboard;
- configuratie starten;
- setupwaarden aanpassen;
- output en geschiedenis tonen.

### 6. Ansible

In dit hoofdstuk komt de Ansible-uitleg:

- inventory per setup;
- playbooks per setup;
- waarom we geen uitgebreide roles gebruiken;
- variabelen uit `info.yml`;
- configuratie van router;
- configuratie van switch;
- configuratie van HTTP-, HTTPS- en FTP-server;
- output en foutmeldingen;
- backups.

### 7. Docker

In dit hoofdstuk komt Docker:

- Dockerfiles;
- `docker-compose.yml`;
- gebruikte poorten;
- volumes;
- netwerken;
- buildproces.

### 8. Beperkingen en MVP-keuzes

In dit hoofdstuk leggen we eerlijk uit:

- wat volledig gebouwd is;
- wat beperkt gebouwd is;
- wat bewust niet gebouwd is;
- waarom dit verdedigbaar is als MVP.


## Daily stand-ups

We plannen opnieuw 4 korte momenten via MS Teams. De focus ligt deze sprint vooral op opleveren, documenteren en demo voorbereiden.

**01/06 Maandag daily 1 | 20:00 | MS Teams**

Bart
Ik heb vooral gekeken welke onderdelen van Ansible, Docker en de netwerkopstellingen nog duidelijker gedocumenteerd moesten worden. Setup1 en setup2 werken technisch, maar de uitleg moest nog beter aansluiten op wat de playbooks echt doen. Mijn volgende stap is het technisch document aanvullen met de infrastructuur, de inventories, de playbooks, Docker Compose en de beperkingen rond EVE-NG. Ik zit niet echt vast, maar we moeten opletten dat de documentatie niet afwijkt van `info.yml`.

Lina
Lina heeft gekeken naar het Flask- en frontendgedeelte. De login, dashboardpagina, geschiedenis, output en backups werken, maar moeten nog duidelijk uitgelegd worden voor de evaluatie. Haar volgende stap is de templates en de dashboardflow documenteren in mensentaal. Ze moet vooral letten op de Jinja2-stukken, zodat duidelijk is waar de data vandaan komt.

Joost
Joost heeft gekeken naar de database en installatiehandleiding. De database werkt met users, network_setups en deployment_logs, maar die tabellen moeten nog duidelijk uitgelegd worden. Zijn volgende stap is de SQLite-werking en de installatie op Debian/Docker beschrijven. Hij moet vooral controleren dat de installatiehandleiding reproduceerbaar blijft.

**02/06 Dinsdag daily 2 | 20:00 | MS Teams**

Bart
Ik heb de Ansible-bestanden verder nagelezen en extra korte commentaar toegevoegd waar dat nuttig was. Vooral `ansible_tools.py`, de inventories en de playbooks moesten goed uitlegbaar zijn. Mijn volgende stap is de technische documentatie verder afstemmen met setup1 en setup2. Het aandachtspunt blijft dat setup2 in de documentatie exact dezelfde interfaces en VLANs moet tonen als in `info.yml`.

Lina
Lina heeft verder gewerkt aan de uitleg van de Flask-flow. De routes, sessies, login, dashboardweergave en history-sectie zijn besproken en gedocumenteerd. Haar volgende stap is de frontenddocumentatie aanvullen met uitleg over status, output, filters en backupdownloads. Er zijn geen grote blokkades meer, maar de uitleg moet kort genoeg blijven.

Joost
Joost heeft de databasecode verder nagelezen en commentaar toegevoegd bij de belangrijkste functies. Zijn volgende stap is uitleg voorzien over `init_database()`, `verify_user()`, `get_network_setups()` en de deployment logs. Hij moet ook duidelijk uitleggen waarom wachtwoorden gehasht worden en waarom deployment logs gekoppeld zijn aan users en setups.

**04/06 Donderdag daily 3 | 20:00 | MS Teams**

Bart
Ik heb de demo-flow mee getest en gekeken of setup1 en setup2 nog overeenkomen met de technische documentatie. Ook de running-config backups werden gecontroleerd als bewijs dat Ansible effectief configuraties uitvoert. Mijn volgende stap is de laatste verbeteringen in het technisch document verwerken. Het moeilijkste blijft testen via EVE-NG, VPN of hotspot omdat het netwerk soms extra vertraging of time-outs veroorzaakt.

Lina
Lina heeft de frontend en diagrammen verder nagekeken. De bedoeling is dat de docent snel ziet welke setup gestart wordt, wat de status is en waar de technische output of backups staan. Haar volgende stap is screenshots/diagrammen en de Flask-uitleg klaarzetten voor het einddocument. Er waren geen grote codeblokkades meer.

Joost
Joost heeft de installatiehandleiding en database-uitleg verder uitgewerkt. De Debian Docker-host, Docker Compose en SQLite-initialisatie moeten reproduceerbaar uitgelegd worden. Zijn volgende stap is de uitleg nog eens controleren door de stappen te volgen. Het aandachtspunt is dat de installatie op een andere machine dezelfde flow moet opleveren.

**05/06 Vrijdag daily 4 | 20:00 | MS Teams**

Bart
Ik heb de laatste eindcontrole gedaan op Ansible, Docker, setupdocumentatie, running-config bewijs, AI-logboek en changelog. Mijn volgende stap is de Sprint 4-retrospective en Scrum-documenten gelijkzetten met de echte eindstatus. Voor de evaluatie moet ik vooral kunnen uitleggen hoe Flask via `ansible_tools.py` Ansible start en hoe backups gekoppeld zijn aan een run.

Lina
Lina heeft haar frontend- en Flaskdocumentatie nagekeken. De dashboardflow, login, outputweergave, geschiedenis en backupdownloads zijn klaar om uitgelegd te worden. Haar volgende stap is de laatste versie klaarzetten en zorgen dat haar changelog en AI-logboek volledig zijn. Voor de evaluatie focust ze op de werking van de applicatie voor de gebruiker.

Joost
Joost heeft zijn databasebestanden en installatie-uitleg nagekeken. De SQLite-tabellen, testgebruikers, password hashing en logs zijn klaar om uitgelegd te worden. Zijn volgende stap is de laatste controle van zijn changelog en AI-logboek. Voor de evaluatie focust hij op hoe de data wordt opgeslagen en opnieuw getoond in de frontend.

Tijdens elke daily bespreken we:

- wat heb ik gedaan?
- wat ga ik nu doen?
- waar zit ik vast?


## Werkende eindversie

Op het einde van Sprint 4 is dit klaar:

- de MVP start opnieuw vanaf de gepushte versie;
- demo-flow is getest;
- technisch document is volledig ingevuld;
- setup1 en setup2 zijn duidelijk gedocumenteerd;
- installatiehandleiding is bruikbaar;
- iedereen kent zijn of haar code;
- AI-logboeken en changelogs zijn nagekeken;
- beperkingen zijn eerlijk beschreven;
- project is klaar voor evaluatie.
