# Retrospective Sprint 1

## Wat ging goed?

- De basis van het project stond vrij snel klaar. De mappenstructuur, templates, databasebestanden, Ansible-bestanden en Dockerbestanden waren duidelijk verdeeld.
- De samenwerking tussen de delen is duidelijker geworden. We weten nu beter wat in `app.py`, `database_tools.py` en `ansible_tools.py` hoort.
- Sprint 1 is eigenlijk sneller gegaan dan verwacht, waardoor we al meer konden testen dan eerst gepland.
- De eerste basisopstelling is effectief getest met EVE-NG. De router, switch en serverplaybooks worden via de Flask-flow gestart.
- De switchplaybook en serverplaybook lopen goed door. De routerplaybook werkt ook na het juist zetten van de managementinterface.
- De koppelafspraken hebben geholpen om dezelfde namen en hetzelfde outputformaat te gebruiken.

## Wat ging moeilijk?

- `app.py` werd eerst wat te groot en deed te veel zelf. Er stond database- en Ansiblelogica in die eigenlijk beter in aparte helperbestanden hoort.
- Docker en Windows-poorten gaven wat problemen bij het starten van de Flask-container.
- Ansible met Cisco vIOS in EVE-NG vroeg extra uitzoekwerk. Vooral SSH, oude algoritmes en Paramiko zorgden voor vertraging.
- De routerconfiguratie gaf eerst problemen omdat de managementinterface per ongeluk mee werd aangepast. Daardoor viel de verbinding soms weg.

## Wat nemen we mee naar sprint 2?

- We moeten de taakverdeling blijven volgen: Lina voor Flask/frontend, Joost voor database/backend en Bart voor Ansible/Docker/netwerk.
- `app.py` moet vooral de webflow doen en niet opnieuw vol SQL of Ansiblecommando's komen te staan.
- Voor Ansible-tests moeten we altijd eerst controleren of router en switch via management-IP en SSH bereikbaar zijn.
- Managementinterfaces moeten apart blijven van labinterfaces. Anders kan Ansible zijn eigen verbinding verbreken.
- Technische problemen zoals oude SSH-algoritmes documenteren we eerlijk, zodat we later nog weten waarom bepaalde keuzes gemaakt zijn.
- We blijven eerst 1 basisopstelling stabiel maken voor we extra opties toevoegen.

## Actiepunten

| Actie | Eigenaar | Tegen wanneer |
| --- | --- | --- |
| Sprintstatussen in `sprint-1.md` nakijken en alles wat klaar is op Done zetten. | Team | Start sprint 2 |
| Changelog en AI-logboek per persoon aanvullen. | Iedereen | Start sprint 2 |
| Databasewerking en deployment logs kort documenteren. | Joost | Sprint 2 |
| Dashboard en Flask-flow nog eens visueel/functioneel controleren. | Lina | Sprint 2 |
| EVE-NG-testopstelling bewaren of duidelijk documenteren zodat we ze later opnieuw kunnen opbouwen. | Bart | Sprint 2 |
| Netwerkdiagram aanmaken volgens labo brussel | Lina | sprint 2 |