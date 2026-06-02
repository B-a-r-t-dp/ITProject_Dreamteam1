# Retrospective Sprint 3

## Wat ging goed?

- Setup2 is toegevoegd als tweede netwerkopstelling. Deze opstelling sluit beter aan bij het labo/pod-verhaal uit de opdracht.
- Elke setup heeft nu een eigen `inventory.ini`. Daardoor blijven de management-IP's per opstelling duidelijk gescheiden.
- De Ansible-helper werkt nu niet meer alleen voor setup1. De juiste setupmap, playbooks en inventory worden gekozen op basis van de setup die gestart wordt.
- De frontend toont nu meerdere opstellingen en de startknop geeft de juiste setup-id door.
- De setupwaarden worden duidelijker getoond en kunnen aangepast worden via een formulier.
- Aangepaste waarden worden eerst gevalideerd en daarna opgeslagen in `info.yml`. Daardoor gebruikt Ansible nadien ook echt de aangepaste waarden.
- De configuratiegeschiedenis is veel bruikbaarder geworden. Per run zien we setup, gebruiker, tijdstip, status, samenvatting, technische output en backups.
- De backups zijn gekoppeld aan de juiste configuratierun. Daardoor is het duidelijk welke running-config bij welke push hoort.
- De geschiedenis kan gefilterd worden op setup en status. Dat maakt het makkelijker om eerdere runs terug te vinden.

## Wat ging moeilijk?

- Setup2 was moeilijker dan setup1, omdat de opgave met pods, switches aan twee kanten en EtherChannel eerst goed begrepen moest worden.
- De EVE-NG-basisconfiguratie moest juist staan voor Ansible kon werken. Vooral SSH en management-IP's moesten eerst goed gecontroleerd worden.
- Binnen EVE-NG was de router soms wel pingbaar, maar SSH werkte niet altijd meteen. Daardoor leek Ansible soms te falen terwijl de basisconfiguratie op het toestel nog niet volledig juist stond.
- De setupvariabelen tonen in de frontend was lastiger dan verwacht. Ruwe YAML-structuren zijn technisch logisch, maar niet leesbaar voor een docent.
- We moesten goed opletten dat aanpasbare waarden niet direct de configuratie pushen. Daarom hebben we bewust gekozen voor eerst opslaan en pas daarna starten via de bestaande knop.
- Sommige Scrum-taken overlapten een beetje. Daardoor moesten we op het einde opnieuw bekijken welke taken echt Done waren en welke beter naar Sprint 4 horen.

## Wat nemen we mee naar Sprint 4?

- Sprint 4 moet geen grote nieuwe implementaties meer bevatten.
- De focus ligt op documentatie, testen, screenshots, demo voorbereiden en code goed kunnen uitleggen.
- De technische documentatie moet duidelijk uitleggen:
  - hoe setup1 aangesloten en geconfigureerd wordt;
  - hoe setup2 aansluit bij het labo/pod-verhaal;
  - hoe Docker, Flask, SQLite en Ansible samenwerken;
  - hoe backups en logs werken.
- We moeten alle teamleden nog goed door de code laten gaan, zodat de focus legt op zijn eigen verantwoordelijke pagina's goed te documenteren zodat we een geheel krijgen dat voor iedereen leesbaar is en iedereen begrijpt.
- De einddemo moet voorbereid worden met een vaste testflow, zodat we niet moeten improviseren tijdens de evaluatie.

## Actiepunten

| Actie | Eigenaar | Tegen wanneer |
| --- | --- | --- |
| Technische documentatie verder afwerken en screenshots toevoegen. | Team | Sprint 4 |
| Volledige demo-flow uitschrijven en testen. | Team | Sprint 4 |
| Code per onderdeel overlopen zodat iedereen zijn deel kan uitleggen. | Bart, Lina en Joost | Sprint 4 |
| Controleren of alle Scrum-documenten overeenkomen met de echte projectstatus. | Team | Sprint 4 |
