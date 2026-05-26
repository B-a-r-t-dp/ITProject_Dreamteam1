# Retrospective Sprint 2

## Wat ging goed?

- De basisflow werkt nu echt als 1 geheel. Een docent kan aanmelden, een opstelling kiezen, op Start configuratie klikken en de Ansible-flow laten lopen.
- De servercontainers zijn veel beter getest. HTTP, HTTPS en FTP worden niet alleen gestart, maar ook gecontroleerd vanuit het serverplaybook.
- De router- en switchplaybooks zijn getest in EVE-NG en gebruiken nu waarden uit `info.yml`. Daardoor is de basisopstelling minder hardcoded.
- De backups van router en switch werken. De running-configs worden bewaard in `backups/` met toestelnaam, docentnaam en timestamp.
- De output op het dashboard is duidelijker geworden. Eerst tonen we een samenvatting, en de ruwe technische output staat achter een uitklapbaar stuk.
- FTP is beter bruikbaar gemaakt voor echte clients zoals WinSCP door passive FTP correct te voorzien.
- De taakverdeling bleef grotendeels duidelijk: Bart werkte vooral aan Ansible/Docker/netwerk, Joost aan database/logging en Lina aan Flask/frontend.

## Wat ging moeilijk?

- FTP was lastiger dan verwacht. Poort 21 alleen was niet genoeg, omdat FTP ook een dataverbinding nodig heeft. Daardoor bleef WinSCP eerst hangen bij het lezen van de map.
- De ruwe Ansible-output was te technisch voor het dashboard. We moesten zoeken naar een oplossing die duidelijker is, maar toch simpel blijft.
- De timestamps zijn nog niet volledig gelijk. Backups gebruiken Belgische tijd, maar SQLite gebruikt standaard nog UTC voor deployment logs.

## Wat nemen we mee naar Sprint 3?

- We gaan de doorschuiftaken rond aanpasbare setupwaarden in Sprint 3 opnemen:
  - PB-77: klein formulier voorzien voor setupwaarden;
  - PB-78: aangepaste waarden doorgeven aan Ansible;
  - PB-79: invoer controleren.
- Voor meerdere opstellingen kiezen we waarschijnlijk voor een eigen `inventory.ini` per setup. Zo kan setup2 andere router- en switch-IP's hebben zonder rare namen zoals `r1_setup2`.
- De dashboard-output moet simpel blijven: samenvatting eerst, technische output als bewijs/debug eronder.
- De deployment log timestamps kunnen in Sprint 3 aangepast worden naar Belgische tijd, zodat dashboard en backupbestanden hetzelfde tijdsgevoel hebben.

## Actiepunten

| Actie | Eigenaar | Tegen wanneer |
| --- | --- | --- |
| PB-77, PB-78 en PB-79 duidelijk opnemen in Sprint 3. | Team | Sprintplanning 3 |
| Beslissen hoe setup2 wordt opgebouwd en of die een eigen inventory krijgt. | Bart + team | Sprint 3 |
| Deployment log timestamps bekijken en eventueel naar Belgische tijd zetten. | Joost + Bart | Sprint 3 |