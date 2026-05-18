# Sprint 1 - Basis en taakverdeling

## Doel

De projectbasis staat klaar en iedereen weet welk deel en welke bestanden van hem/haar zijn.

## Gekozen backlogtaken

| PB-ID | Taak | Eigenaar | Bestand(en) | Status |
| --- | --- | --- | --- | --- |
| PB-01 | Projectstructuur controleren | Team | `README.md`, alle hoofdmappen | Done |
| PB-02 | Opstartdocument bespreken | Team | `docs/opstartdocument.md` | Done |
| PB-03 | MVP-afbakening bespreken | Team | `docs/mvp-afbakening.md` | Done |
| PB-04 | Scope over de sprints bespreken | Team | `docs/scrum/scope-4-sprints.md` | Done |
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
Bart
Ik heb vooral gekeken naar mijn deel van het project: Ansible, Docker en de netwerkbestanden. De inventory, playbooks en Dockerbestanden stonden al klaar als basis. Ik ga nu verder bekijken wat er nog beter voorbereid moet worden voor EVE-NG (emulatie) en hoe we dit duidelijk kunnen documenteren. Ik zit nog niet echt vast, maar we moeten wel goed afspreken hoe ver de playbooks al moeten gaan in deze sprint.

Lina
Lina heeft gewerkt aan de loginpagina en het dashboard. De basispagina’s staan klaar en er is al plaats voorzien om netwerkopstellingen en output te tonen. De volgende stap is zorgen dat het dashboard de juiste data krijgt vanuit Flask. Er moest nog afgestemd worden welke data precies uit de database en uit Ansible komt.

Joost
Joost heeft de SQLite-tabellen voorbereid. De tabellen voor gebruikers, netwerkopstellingen en deployment logs zijn voorzien. De volgende stap is functies maken om die data vanuit Flask te kunnen gebruiken. Er moest nog afgesproken worden hoe de output van Ansible exact opgeslagen wordt in SQLite.

**13/05 Woensdag daily 2 | 20:00 | MS Teams - bericht |**
Bart
Ik heb mijn Ansible-deel verder voorbereid. De inventory is afgestemd op de router en switch in EVE-NG en de playbooks zijn duidelijker uitgewerkt. Ook de Dockerfiles en Docker Compose zijn nagekeken. Mijn volgende stap is de Ansible-helper klaarmaken, zodat Flask later gewoon run_setup() kan gebruiken. Waar ik rekening mee moet houden, is dat de router en switch eerst een management-IP en SSH nodig hebben voor Ansible kan werken.

Lina
Lina heeft verder gekeken naar de Flask-routes voor login, dashboard en logout. Het dashboard wordt achter login gezet. De volgende stap is app.py netter maken, zodat daar niet alle SQL en Ansible-code rechtstreeks in staat. Dat moest nog afgestemd worden met Joost en Bart, omdat database en Ansible eigenlijk in aparte helperbestanden horen.

Joost
Joost heeft verder gewerkt aan de databasehelper. Functies zoals database initialiseren, gebruiker controleren, netwerkopstellingen ophalen en logs opslaan zijn voorbereid. De volgende stap is zorgen dat er automatisch een testdocent en een basisopstelling in de database komen. Er moest nog duidelijk afgesproken worden dat de status van Ansible altijd success of failed is.

**15/05 Vrijdag daily 3 | 19:00 | MS Teams |**
Ik heb modules/ansible_tools.py verder uitgewerkt. De functie run_setup() start nu de router-, switch- en serverplaybooks en geeft altijd status en output terug. Dat past bij de koppelafspraken met Flask en SQLite. Mijn volgende stap is dit testen met de EVE-NG-router en switch. Waar ik nog tegenaan liep, waren oude SSH-instellingen op de Cisco-images en dependencies in de Docker-container.

Lina
Lina heeft app.py opgeschoond zodat die vooral de Flask-flow doet: routes, sessies en templates tonen. De databasecode gaat via Joost zijn helper en Ansible via Bart zijn helper. De volgende stap is het dashboard duidelijker en professioneler maken. Ze is daarbij afhankelijk van de juiste databasefuncties en de output van Ansible.

Joost
Joost heeft ervoor gezorgd dat de database automatisch kan worden aangemaakt vanuit het schema. Er wordt ook een testdocent voorzien en minstens één basisopstelling. De volgende stap is controleren of deployment logs goed worden opgeslagen na een configuratierun. Er waren geen grote blokkades meer, vooral nog testen met echte output.

**16/05 Zaterdag daily 4 | 13:00 | MS Teams |**
Bart
Ik heb de EVE-NG-router en switch getest met Ansible. De switchplaybook loopt volledig door en de routerplaybook configureert nu de labinterface en OSPF-basis. Ook het serverplaybook loopt door en geeft output terug. Mijn volgende stap is de testresultaten documenteren en kort noteren welke problemen we hadden met oude SSH-algoritmes en Paramiko. Voor Sprint 1 zit ik niet meer vast.

Lina
Lina heeft het dashboard professioneler gemaakt. Je ziet nu duidelijk de gebruiker, beschikbare opstellingen, laatste status en Ansible-output. De loginpagina is behouden met de bestaande achtergrond. De volgende stap is nog een laatste visuele controle zodat de demo duidelijk toonbaar is. Er is geen grote blokkade meer.

Joost
Joost heeft gecontroleerd dat login, basisopstelling en deployment logging samen werken met Flask. De database bevat de nodige tabellen en testdata. De volgende stap is de databasewerking kort documenteren en nakijken of logs goed bewaard blijven. Er is geen grote blokkade meer.



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