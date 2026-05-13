# Changelog Bart

| Datum | Sprint | Bestand(en) | Wijziging | Waarom |
| --- | --- | --- | --- | --- |
| 2026-05-07 | Sprint week 1 | Projectstructuur | Compact startsjabloon opgezet. | Om opnieuw te starten met een duidelijke MVP-basis. |
| 2026-05-07 | Sprint 1 | `docs/scope-4-sprints.md`, `docs/scrum/`, `README.md`, `docs/opstartdocument.md` | 4-sprint scope, sprintbestanden, retrospectives en uitgebreide product backlog toegevoegd. | Zodat elke stap voor de MVP in de backlog staat en per sprint opgevolgd kan worden. |
| 2026-05-12 | Sprint 1 | `ansible/inventory.ini` | Inventory gecontroleerd en voorbereid met groepen voor router, switch en gedeelde netwerkdevice-instellingen. | Zodat Ansible later duidelijk weet welke EVE-NG-toestellen aangesproken worden. |
| 2026-05-12 | Sprint 1 | `ansible/playbooks/router.yml`, `ansible/playbooks/switch.yml`, `ansible/playbooks/servers.yml` | Playbooks inhoudelijk voorbereid voor router, switch en servercontainers. | Zodat de MVP-flow al aansluit op router, switch, HTTP, HTTPS en FTP, ook al moet echte EVE-NG-test later gebeuren. |
| 2026-05-12 | Sprint 1 | `Dockerfile`, `docker-compose.yml`, `servers/http/`, `servers/https/`, `servers/ftp/` | Docker- en servercontainerbestanden nagekeken en gedocumenteerd. | Zodat de Flask-, HTTP-, HTTPS- en FTP-containers uitlegbaar en testbaar zijn. |
| 2026-05-12 | Sprint 1 | `modules/ansible_tools.py`, `docs/koppelafspraken.md` | Ansible-helper afgestemd op vast `status`/`output`-formaat en koppelafspraken uitgebreid. | Zodat Flask, SQLite en Ansible hetzelfde outputformaat gebruiken. |
| 2026-05-12 | Sprint 1 | `app.py`, `modules/database_tools.py`, `modules/ansible_tools.py` | Projectarchitectuur mee geanalyseerd en afgestemd op de taakverdeling tussen Flask, SQLite en Ansible. | Zodat `app.py` vooral de webflow doet en database/Ansible-logica in de juiste modules blijft. |
| 2026-05-12 | Sprint 1 | `templates/dashboard.html`, `static/style.css` | Dashboard visueel verbeterd en CSS gescheiden tussen loginpagina en dashboard. | Zodat de demo professioneler oogt zonder de bestaande loginachtergrond te verliezen. |
