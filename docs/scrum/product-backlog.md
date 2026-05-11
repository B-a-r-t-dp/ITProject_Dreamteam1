# Product Backlog

De product backlog bevat alle stappen die nodig zijn om de haalbare MVP te realiseren.

De backlog is afgestemd op:

```text
docs/scope-4-sprints.md
```

## Must have

| ID | Sprint | Taak | Eigenaar | Status |
| --- | --- | --- | --- | --- |
| PB-01 | Sprint 1 | Projectstructuur controleren | Team | To do |
| PB-02 | Sprint 1 | Opstartdocument bespreken | Team | To do |
| PB-03 | Sprint 1 | MVP-afbakening bespreken | Team | To do |
| PB-04 | Sprint 1 | Scope over 4 sprints bespreken | Team | To do |
| PB-05 | Sprint 1 | Taakverdeling en bestandseigenaars bevestigen | Team | To do |
| PB-06 | Sprint 1 | AI-logboek, changelog en koppelafspraken uitleggen | Team | To do |
| PB-07 | Sprint 1 | Loginpagina als template klaarzetten | Lina | To do |
| PB-08 | Sprint 1 | Dashboardpagina als template klaarzetten | Lina | To do |
| PB-09 | Sprint 1 | Plaats voorzien voor netwerkopstellingen op dashboard | Lina | To do |
| PB-10 | Sprint 1 | Plaats voorzien voor status/output op dashboard | Lina | To do |
| PB-11 | Sprint 1 | SQLite-schema voor `users` uitwerken | Joost | To do |
| PB-12 | Sprint 1 | SQLite-schema voor `network_setups` uitwerken | Joost | To do |
| PB-13 | Sprint 1 | SQLite-schema voor `deployment_logs` uitwerken | Joost | To do |
| PB-14 | Sprint 1 | Relaties tussen tabellen voorbereiden | Joost | To do |
| PB-15 | Sprint 1 | Ansible-inventory invullen met router en switch | Bart | To do |
| PB-16 | Sprint 1 | Routerplaybook als basis voorbereiden | Bart | To do |
| PB-17 | Sprint 1 | Switchplaybook als basis voorbereiden | Bart | To do |
| PB-18 | Sprint 1 | Serverplaybook als basis voorbereiden | Bart | To do |
| PB-19 | Sprint 1 | Flask Dockerfile controleren | Bart | To do |
| PB-20 | Sprint 1 | Docker Compose controleren | Bart | To do |
| PB-21 | Sprint 1 | HTTP Dockerfile controleren | Bart | To do |
| PB-22 | Sprint 1 | HTTPS Dockerfile controleren | Bart | To do |
| PB-23 | Sprint 1 | FTP Dockerfile controleren | Bart | To do |
| PB-24 | Sprint 2 | SQLite-database initialiseren vanuit schema | Joost | To do |
| PB-25 | Sprint 2 | Testdocent aanmaken | Joost | To do |
| PB-26 | Sprint 2 | Password hashing toepassen voor testdocent | Joost | To do |
| PB-27 | Sprint 2 | Minstens 1 netwerkopstelling opslaan in SQLite | Joost | To do |
| PB-28 | Sprint 2 | Functie maken om users te controleren | Joost | To do |
| PB-29 | Sprint 2 | Functie maken om network_setups op te halen | Joost | To do |
| PB-30 | Sprint 2 | Functie maken om deployment_logs op te slaan | Joost | To do |
| PB-31 | Sprint 2 | Loginroute koppelen aan SQLite | Lina + Joost | To do |
| PB-32 | Sprint 2 | Logout voorzien | Lina | To do |
| PB-33 | Sprint 2 | Dashboard beschermen achter login | Lina | To do |
| PB-34 | Sprint 2 | Netwerkopstelling tonen op dashboard | Lina + Joost | To do |
| PB-35 | Sprint 2 | Ansible-helper voorbereiden met `status` en `output` | Bart | To do |
| PB-36 | Sprint 2 | Afspraak maken over outputformaat tussen Ansible, Flask en SQLite | Team | To do |
| PB-37 | Sprint 3 | Startknop koppelen aan Flask-route | Lina | To do |
| PB-38 | Sprint 3 | Flask-route koppelen aan Ansible-helper | Lina + Bart | To do |
| PB-39 | Sprint 3 | Ansible-output opslaan in `deployment_logs` | Joost + Bart | To do |
| PB-40 | Sprint 3 | Laatste status/output tonen op dashboard | Lina + Joost | To do |
| PB-41 | Sprint 3 | HTTP-container bereikbaar maken op poort 80 | Bart | To do |
| PB-42 | Sprint 3 | HTTPS-container bereikbaar maken op poort 443 | Bart | To do |
| PB-43 | Sprint 3 | Self-signed certificaat voor HTTPS voorzien | Bart | To do |
| PB-44 | Sprint 3 | FTP-container bereikbaar maken op poort 20/21 | Bart | To do |
| PB-45 | Sprint 3 | FTP-gebruiker en testbestand voorzien | Bart | To do |
| PB-46 | Sprint 3 | Routerplaybook testen of aantoonbaar voorbereiden | Bart | To do |
| PB-47 | Sprint 3 | Switchplaybook testen of aantoonbaar voorbereiden | Bart | To do |
| PB-48 | Sprint 3 | Docker Compose build/start testen | Bart | To do |
| PB-49 | Sprint 4 | Volledige demo-flow testen | Team | To do |
| PB-50 | Sprint 4 | Testen of `main` een werkende sprintversie bevat | Team | To do |
| PB-51 | Sprint 4 | Docker Compose build/start documenteren | Bart | To do |
| PB-52 | Sprint 4 | SQLite-tabellen en logs documenteren | Joost | To do |
| PB-53 | Sprint 4 | Flask-flow documenteren | Lina | To do |
| PB-54 | Sprint 4 | Netwerk/Ansible-beperkingen documenteren | Bart | To do |
| PB-55 | Sprint 4 | MVP-afbakening finaliseren | Team | To do |
| PB-56 | Sprint 4 | Niet-afgewerkte onderdelen verantwoorden | Team | To do |
| PB-57 | Sprint 4 | Presentatie/demo voorbereiden | Team | To do |
| PB-58 | Sprint 4 | AI-logboeken en changelogs controleren | Team | To do |

## Could have

Alleen opnemen als de Must have-taken van die sprint werken.

| ID | Sprint | Taak | Eigenaar | Status |
| --- | --- | --- | --- | --- |
| PB-59 | Sprint 2 | Dashboard iets mooier maken | Lina | To do |
| PB-60 | Sprint 3 | Ansible-output duidelijker formatteren | Lina + Bart | To do |
| PB-61 | Sprint 3 | Extra foutmelding tonen bij Ansible-fout | Lina + Bart | To do |
| PB-62 | Sprint 4 | Tweede netwerkopstelling als voorbeeld toevoegen | Joost + Lina | To do |

## Niet in MVP

| Onderdeel | Reden |
| --- | --- |
| Adminpagina | Te groot voor de basis. |
| Realtime Ansible-output | Bonus en technisch complexer. |
| CI/CD | Bonus, geen kern van de demo. |
| Volledig labo tegelijk configureren | Te groot voor beschikbare tijd. |
| Productie-security | We doen basisveiligheid, geen productieplatform. |
