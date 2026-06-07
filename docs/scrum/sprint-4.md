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
- Iedereen moet elke lijn code in heel het project kennen.. dus het is belangrijk dat we optijd pushen zodat we altijd op de nieuwste versie zitten.


## Gekozen taken sprint 4

| PB-ID | Taak | Wat betekent dit concreet? | Eigenaar | Bestand(en) | Status |
| --- | --- | --- | --- | --- | --- |
| PB-49 | Volledige demo-flow testen | We testen de demo alsof de docent meekijkt: login, setup kiezen, waarden aanpassen, configuratie starten, output bekijken, geschiedenis controleren en backups downloaden. | Team | volledige project | To do |
| PB-50 | Testen of `main` een werkende sprintversie bevat | We controleren of de gepushte versie opnieuw kan starten vanaf een propere checkout. | Team | GitHub, Docker Compose | To do |
| PB-51 | Docker Compose build/start documenteren | De stappen om Docker-images te bouwen en containers te starten worden duidelijk uitgelegd. | Bart | `Dockerfile`, `docker-compose.yml`, `servers/`, technisch document | Done |
| PB-52 | SQLite-tabellen en logs documenteren | De database, tabellen, gebruikers, setupdata en deployment logs worden duidelijk uitgelegd. | Joost | `database/schema.sql`, `modules/database_tools.py`, technisch document | To do |
| PB-53 | Flask-flow documenteren | De login, dashboardflow, routes, templates en frontendwerking worden duidelijk gedocumenteerd. | Lina | `app.py`, `templates/`, `static/`, technisch document | To do |
| PB-54 | Netwerk/Ansible-beperkingen documenteren | We leggen uit wat setup1 en setup2 configureren, welke basisconfiguratie nodig is en wat bewust beperkt blijft. | Bart | `ansible/playbooks/`, setupdocumentatie, technisch document | Done |
| PB-55 | MVP-afbakening finaliseren | We controleren of de MVP-afbakening overeenkomt met wat echt gebouwd is. | Team | `docs/mvp-afbakening.md`, technisch document | To do |
| PB-56 | Niet-afgewerkte onderdelen verantwoorden | Alles wat niet volledig uit de opgave gebouwd is, wordt eerlijk verantwoord als MVP-keuze. | Team | technisch document | To do |
| PB-57 | Presentatie/demo voorbereiden | We maken een vaste demo-volgorde zodat we tijdens de evaluatie niet moeten improviseren. | Team | demo-checklist, technisch document | To do |
| PB-58 | AI-logboeken en changelogs controleren | Iedereen controleert of zijn of haar AI-logboek en changelog volledig en verdedigbaar zijn. | Team | `docs/personen/` | To do |
| PB-96 | Code per eigenaar nalezen en kort documenteren | Iedereen leest zijn eigen bestanden na en voegt waar nodig korte commentaar toe zodat de code begrijpbaar is. | Team | projectbestanden per eigenaar | To do |
| PB-97 | Technisch document als einddocument afwerken | Het technische document wordt ingevuld volgens de opgave en samengebracht tot 1 verhaal. | Team | `technische-documentatie.docx` | To do |


## Status Bart - Sprint 4

Deze Sprint 4-onderdelen zijn voor Bart afgerond:

- PB-51: Docker Compose build/start is uitgewerkt in het technisch document.
- PB-54: Netwerk- en Ansible-beperkingen zijn uitgewerkt voor setup1 en setup2.
- PB-58: Bart zijn AI-logboek en changelog zijn nagekeken en aangevuld.
- PB-96: Bart zijn Ansible-, Docker- en setupbestanden zijn nagelezen en kort gedocumenteerd.
- PB-97: Bart zijn deel van het technisch document is aangevuld en afgestemd op het project.

De teamtaken blijven pas volledig Done wanneer Lina en Joost hun deel ook bevestigd hebben.

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

| Moment | Tijdstip | Medium | Korte notities |
| --- | --- | --- | --- |
| Maandag daily 1 | 20:00 | MS Teams | Sprint 4 opstarten, taken verdelen en documentatiestructuur bevestigen. |
| Dinsdag daily 2 | 20:00 | MS Teams | Iedereen geeft status van zijn documentatiedeel en eventuele code-uitleg. |
| Donderdag daily 3 | 20:00 | MS Teams | Demo-flow testen, screenshots/testbewijs verzamelen en open punten bespreken. |
| Vrijdag daily 4 | 20:00 | MS Teams | Eindcontrole: technisch document, Scrum-documenten, changelogs, AI-logboeken en demo. |

Tijdens elke daily bespreken we:

- wat heb ik gedaan?
- wat ga ik nu doen?
- waar zit ik vast?


## Werkende eindversie

Op het einde van Sprint 4 moet dit klaar zijn:

- de MVP start opnieuw vanaf de gepushte versie;
- demo-flow is getest;
- technisch document is volledig ingevuld;
- setup1 en setup2 zijn duidelijk gedocumenteerd;
- installatiehandleiding is bruikbaar;
- iedereen kent zijn of haar code;
- AI-logboeken en changelogs zijn nagekeken;
- beperkingen zijn eerlijk beschreven;
- project is klaar voor evaluatie.
