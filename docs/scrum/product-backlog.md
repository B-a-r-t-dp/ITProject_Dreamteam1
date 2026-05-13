# Product Backlog

De product backlog bevat de stappen die nodig zijn om een haalbare MVP op te leveren.

Na Sprint 1 hebben we gemerkt dat de basis sneller klaar was dan verwacht. Daarom breiden we de MVP licht uit richting de opgave, maar zonder grote extra modules toe te voegen.

De planning is afgestemd op:

```text
docs/scrum/scope-4-sprints.md
```

## Must have

| ID | Sprint | Taak | Eigenaar | Status |
| --- | --- | --- | --- | --- |
| PB-01 | Projectstructuur controleren | Team | Done |
| PB-02 | Opstartdocument bespreken | Team | Done |
| PB-03 | MVP-afbakening bespreken | Team | Done |
| PB-04 | Scope over 4 sprints bespreken | Team | Done |
| PB-05 | Taakverdeling en bestandseigenaars bevestigen | Team | Done |
| PB-06 | AI-logboek, changelog en koppelafspraken uitleggen | Team | Done |
| PB-07 | Loginpagina als template klaarzetten | Lina | Done |
| PB-08 | Dashboardpagina als template klaarzetten | Lina | Done |
| PB-09 | Plaats voorzien voor netwerkopstellingen op dashboard | Lina | Done |
| PB-10 | Plaats voorzien voor status/output op dashboard | Lina | Done |
| PB-11 | SQLite-schema voor `users` uitwerken | Joost | Done |
| PB-12 | SQLite-schema voor `network_setups` uitwerken | Joost | Done |
| PB-13 | SQLite-schema voor `deployment_logs` uitwerken | Joost | Done |
| PB-14 | Relaties tussen tabellen voorbereiden | Joost | Done |
| PB-15 | Ansible-inventory invullen met router en switch | Bart | Done |
| PB-16 | Routerplaybook als basis voorbereiden | Bart | Done |
| PB-17 | Switchplaybook als basis voorbereiden | Bart | Done |
| PB-18 | Serverplaybook als basis voorbereiden | Bart | Done |
| PB-19 | Flask Dockerfile controleren | Bart | Done |
| PB-20 | Docker Compose controleren | Bart | Done |
| PB-21 | HTTP Dockerfile controleren | Bart | Done |
| PB-22 | HTTPS Dockerfile controleren | Bart | Done |
| PB-23 | FTP Dockerfile controleren | Bart | Done |
| PB-24 | SQLite-database initialiseren vanuit schema | Joost | Done |
| PB-25 | Testdocent aanmaken | Joost | Done |
| PB-26 | Password hashing toepassen voor testdocent | Joost | Done |
| PB-27 | Minstens 1 netwerkopstelling opslaan in SQLite | Joost | Done |
| PB-28 | Functie maken om users te controleren | Joost | Done |
| PB-29 | Functie maken om network_setups op te halen | Joost | Done |
| PB-30 | Functie maken om deployment_logs op te slaan | Joost | Done |
| PB-31 | Loginroute koppelen aan SQLite | Lina + Joost | Done |
| PB-32 | Logout voorzien | Lina | Done |
| PB-33 | Dashboard beschermen achter login | Lina | Done |
| PB-34 | Netwerkopstelling tonen op dashboard | Lina + Joost | Done |
| PB-35 | Ansible-helper voorbereiden met `status` en `output` | Bart | Done |
| PB-36 | Afspraak maken over outputformaat tussen Ansible, Flask en SQLite | Team | Done |
| PB-67 | Playbooks groeperen per netwerkopstelling in `setup1` | Bart | Done |
| PB-68 | Extra setupinformatie tonen op dashboard vanuit `setup1/info.yml` | Lina + Bart | Done |
| PB-37 | Startknop koppelen aan Flask-route | Lina | To do |
| PB-38 | Flask-route koppelen aan Ansible-helper | Lina + Bart | To do |
| PB-39 | Ansible-output opslaan in `deployment_logs` | Joost + Bart | To do |
| PB-40 | Laatste status/output tonen op dashboard | Lina + Joost | To do |
| PB-41 | HTTP-container bereikbaar maken op poort 80 | Bart | To do |
| PB-42 | HTTPS-container bereikbaar maken op poort 443 | Bart | To do |
| PB-43 | Self-signed certificaat voor HTTPS voorzien | Bart | To do |
| PB-44 | FTP-container bereikbaar maken op poort 20/21 | Bart | To do |
| PB-45 | FTP-gebruiker en testbestand voorzien | Bart | To do |
| PB-46 | Routerplaybook testen of aantoonbaar voorbereiden | Bart | To do |
| PB-47 | Switchplaybook testen of aantoonbaar voorbereiden | Bart | To do |
| PB-48 | Docker Compose build/start testen | Bart | To do |
| PB-63 | IP-adresseringsschema opstellen voor de basisopstelling | Bart | To do |
| PB-69 | `info.yml` uitbreiden met configureerbare setupvariabelen | Bart | To do |
| PB-70 | Routerplaybook variabel maken op basis van setupdata | Bart | To do |
| PB-71 | Switchplaybook variabel maken op basis van setupdata | Bart | To do |
| PB-72 | Backupmap gebruiken voor router- en switchconfiguraties | Bart | To do |
| PB-73 | Running-config backup van router ophalen via Ansible | Bart | To do |
| PB-74 | Running-config backup van switch ophalen via Ansible | Bart | To do |
| PB-75 | Dashboard tonen welke setupwaarden gebruikt worden | Lina + Bart | To do |
| PB-76 | Koppelafspraken bijwerken voor setupdata en backups | Team | To do |
| PB-60 | Ansible-output duidelijker formatteren | Lina + Bart | To do |
| PB-61 | Extra foutmelding tonen bij Ansible-fout | Lina + Bart | To do |
| PB-64 | Netwerkschema/podschema opstellen | Team | To do |
| PB-65 | Serverplaybook uitbreiden met eenvoudige servercontroles | Bart | To do |
| PB-66 | Deployment logs per docent controleren | Joost + Lina | To do |
| PB-77 | Frontendformulier voorzien om setupvariabelen aan te passen | Lina + Bart | To do |
| PB-78 | Aangepaste setupwaarden doorgeven aan Ansible | Bart + Joost | To do |
| PB-79 | Invoer controleren voor IP-adressen, VLANs en hostnames | Joost + Bart | To do |
| PB-49 | Volledige demo-flow testen | Team | To do |
| PB-50 | Testen of `main` een werkende sprintversie bevat | Team | To do |
| PB-51 | Docker Compose build/start documenteren | Bart | To do |
| PB-52 | SQLite-tabellen en logs documenteren | Joost | To do |
| PB-53 | Flask-flow documenteren | Lina | To do |
| PB-54 | Netwerk/Ansible-beperkingen documenteren | Bart | To do |
| PB-55 | MVP-afbakening finaliseren | Team | To do |
| PB-56 | Niet-afgewerkte onderdelen verantwoorden | Team | To do |
| PB-57 | Presentatie/demo voorbereiden | Team | To do |
| PB-58 | AI-logboeken en changelogs controleren | Team | To do |

## Could have

Alleen opnemen als de Must have-taken van die sprint werken.

| ID | Sprint | Taak | Eigenaar | Status |
| --- | --- | --- | --- | --- |
| PB-59 | Dashboard iets mooier maken | Lina | To do |
| PB-62 | Tweede netwerkopstelling als voorbeeld toevoegen | Joost + Lina | To do |

## Niet in MVP

| Onderdeel | Reden |
| --- | --- |
| Adminpagina | Te groot voor de basis. |
| Realtime Ansible-output | Bonus en technisch complexer. |
| CI/CD | Bonus, geen kern van de demo. |
| Volledig labo tegelijk configureren | Te groot; focus op 1 router, 1 switch en 3 servercontainers. |
| Productie-security | We doen basisveiligheid, geen productieplatform. |
| Uitgebreide Ansible roles | Eenvoudige playbooks zijn beter uitlegbaar. |
