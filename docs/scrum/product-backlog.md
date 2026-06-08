# Product Backlog

De product backlog bevat de stappen die nodig zijn om een haalbare MVP op te leveren.

Na Sprint 1 hebben we gemerkt dat de basis sneller klaar was dan verwacht. Daarom breiden we de MVP licht uit richting de opgave, maar zonder grote extra modules toe te voegen.


## Must have

| ID | Taak | Eigenaar | Status |
| --- | --- | --- | --- |
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
| PB-15 | Inventory voor basisopstelling invullen met router en switch | Bart | Done |
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
| PB-37 | Startknop op het dashboard laten werken | Lina | Done |
| PB-38 | Flask de Ansible-helper laten starten | Lina | Done |
| PB-39 | Resultaat van Ansible opslaan in SQLite | Joost | Done |
| PB-40 | Laatste run tonen op het dashboard | Lina | Done |
| PB-41 | HTTP-container starten en testen | Bart | Done |
| PB-42 | HTTPS-container testen | Bart | Done |
| PB-43 | Self-signed certificaat voorzien voor HTTPS | Bart | Done |
| PB-44 | FTP-container testen | Bart | Done |
| PB-45 | FTP-gebruiker en testbestand voorzien | Bart | Done |
| PB-46 | Routerplaybook testen in EVE-NG | Bart | Done |
| PB-47 | Switchplaybook testen in EVE-NG | Bart | Done |
| PB-48 | Docker Compose opnieuw bouwen en starten | Bart | Done |
| PB-63 | IP-adressering van de basisopstelling uitschrijven | Bart | Done |
| PB-69 | `info.yml` uitbreiden met basiswaarden | Bart | Done |
| PB-70 | Routerplaybook laten werken met waarden uit de setup | Bart | Done |
| PB-71 | Switchplaybook laten werken met waarden uit de setup | Bart | Done |
| PB-72 | Backupmap gebruiken | Bart | Done |
| PB-73 | Routerconfiguratie als backup bewaren | Bart | Done |
| PB-74 | Switchconfiguratie als backup bewaren | Bart | Done |
| PB-75 | Op dashboard tonen welke waarden gebruikt worden | Lina | Done |
| PB-76 | Koppelafspraken bijwerken voor setupdata en backups | Team | Done |
| PB-60 | Ansible-output leesbaarder maken | Lina | Done |
| PB-61 | Fouten duidelijker tonen | Lina | Done |
| PB-64 | Netwerkschema of podschema maken | Lina | To do |
| PB-65 | Serverplaybook nuttiger maken | Bart | Done |
| PB-66 | Logs per docent controleren | Joost | Done |
| PB-77 | Klein formulier voorzien voor setupwaarden | Lina | Done |
| PB-78 | Aangepaste waarden doorgeven aan Ansible | Joost | Done |
| PB-79 | Invoer controleren | Joost | Done |
| PB-80 | Deployment log timestamps in Belgische tijd tonen | Lina | Done |
| PB-81 | Configuratiegeschiedenis tonen op dashboard | Lina | Done |
| PB-82 | Samenvatting en technische output per log bekijken | Lina | Done |
| PB-83 | Tweede netwerkopstelling toevoegen volgens labo Brussel | Bart | Done |
| PB-84 | Inventory per netwerkopstelling voorzien | Bart | Done |
| PB-85 | Ansible-helper uitbreiden voor meerdere setupmappen | Bart | Done |
| PB-86 | Dashboard meerdere opstellingen laten tonen en starten | Bart | Done |
| PB-87 | Configuratiegeschiedenis overzichtelijker maken | Team | Done |
| PB-91 | Alleen veilige variabelen aanpasbaar maken | Joost | Done |
| PB-92 | Backupbestanden tonen bij succesvolle configuraties | Lina | Done |
| PB-93 | Backupbestanden logisch ordenen | Bart | Done |
| PB-94 | Sprint 3 eindflow testen | Team | Done |
| PB-95 | Restpunten voor Sprint 4 oplijsten | Team | Done |
| PB-49 | Volledige demo-flow testen | Team | Done |
| PB-50 | Testen of `main` een werkende sprintversie bevat | Team | Done |
| PB-51 | Docker Compose build/start documenteren | Bart | Done |
| PB-52 | SQLite-tabellen en logs documenteren | Joost | Done |
| PB-53 | Flask-flow documenteren | Lina | Done |
| PB-54 | Netwerk/Ansible-beperkingen documenteren | Bart | Done |
| PB-55 | MVP-afbakening finaliseren | Team | Done |
| PB-56 | Niet-afgewerkte onderdelen verantwoorden | Team | Done |
| PB-57 | Presentatie/demo voorbereiden | Team | Done |
| PB-58 | AI-logboeken en changelogs controleren | Team | Done |
| PB-96 | Code per eigenaar nalezen en kort documenteren | Team | Done |
| PB-97 | Technisch document als einddocument afwerken | Team | Done |

## Could have

Alleen opnemen als de Must have-taken van die sprint werken.

| ID | Taak | Eigenaar | Status |
| --- | --- | --- | --- |
| PB-59 | Dashboard iets mooier maken | Lina | To do |
| PB-62 | Extra netwerkopstelling als bonus toevoegen | Joost + Lina | To do |
| PB-88 | Backupbestanden downloadbaar maken | Lina + Bart | Done |
| PB-89 | Output nog verder opdelen per playbook | Lina + Bart | To do |

## Niet in MVP

| Onderdeel | Reden |
| --- | --- |
| Adminpagina | Te groot voor de basis. |
| Realtime Ansible-output | Bonus en technisch complexer. |
| CI/CD | Bonus, geen kern van de demo. |
| Uitgebreide Ansible roles | Eenvoudige playbooks zijn beter uitlegbaar. |

