# Sprint 3 - MVP afwerken en tweede opstelling voorbereiden

## Doel

In Sprint 2 hebben we ervoor gezorgd dat de basis-MVP technisch werkt.


Sprint 3 gebruiken we om de applicatie echt bruikbaar af te werken.

Het doel van Sprint 3 is:

```text
Alles wat we technisch al hebben, beter benutten in de frontend
en een tweede netwerkopstelling voorbereiden volgens het labo in Brussel. 
```

Sprint 3 draait dus rond 3 grote delen:

1. een tweede opstelling volgens labo Brussel / pod-opgave;
2. setupvariabelen mooier tonen en beperkt aanpasbaar maken;
3. configuratiegeschiedenis, output en backups volledig tonen.


## Gekozen backlogtaken sprint 3

| PB-ID | Taak | Wat betekent dit concreet? | Eigenaar | Bestand(en) | Status |
| --- | --- | --- | --- | --- | --- |
| PB-83 | Tweede netwerkopstelling toevoegen volgens labo Brussel | We maken een tweede opstelling die aansluit bij het labo/pod-verhaal uit de opgave. Dit hoeft niet groter te worden dan nodig, maar moet wel duidelijk tonen hoe de tweede opstelling verschilt van setup1. | Bart | `ansible/playbooks/setup2/`, `database/`, `docs/` | Done |
| PB-84 | Inventory per netwerkopstelling voorzien | Elke setup krijgt een eigen `inventory.ini`. Zo kan setup1 bijvoorbeeld `192.168.0.215` gebruiken en setup2 andere management-IP's. De namen `r1` en `sw1` blijven dan rollen binnen die setup. | Bart | `ansible/playbooks/setup1/inventory.ini`, `ansible/playbooks/setup2/inventory.ini`, `modules/ansible_tools.py` | Done |
| PB-85 | Ansible-helper uitbreiden voor meerdere setupmappen | `run_setup()` mag niet hardcoded alleen setup1 starten. De helper moet op basis van de gekozen setup de juiste map, playbooks en inventory gebruiken. | Bart | `modules/ansible_tools.py`, `modules/database_tools.py` | Done |
| PB-86 | Dashboard meerdere opstellingen laten tonen en starten | Het dashboard moet setup1 en setup2 tonen. Elke opstelling toont haar eigen info en de startknop moet de juiste setup-id doorgeven. | Bart | `templates/dashboard.html`, `modules/database_tools.py`, `app.py` | Done |
| PB-77 | Klein formulier voorzien voor variabelen | De docent ziet de variabelen niet meer als ruwe lijst of array, maar in een duidelijk formulier of overzicht. Eerst mag dit vooral zichtbaar zijn, daarna zorgen dat de variabelen beperkt aanpasbaar zijn. | joost | `templates/dashboard.html`, `static/style.css`, `app.py` | Done |
| PB-78 | Aangepaste waarden doorgeven aan Ansible | Als een waarde aangepast wordt, moet die ook gebruikt worden door Ansible. We slaan de gevalideerde waarden op in `info.yml`, zodat Ansible nadien dezelfde waarden gebruikt. | Joost | `modules/database_tools.py`, `modules/ansible_tools.py`, `app.py` | Done |
| PB-79 | Validatie voorzien op de variabelen | Voor we waarden opslaan, controleren we simpele fouten. Bijvoorbeeld geen lege hostname, VLAN-ID moet een nummer zijn en IP-adres moet geldig zijn. | Joost | `modules/database_tools.py`, `app.py` | Done |
| PB-91 | Alleen veilige variabelen aanpasbaar maken | Niet alles uit `info.yml` moet aanpasbaar zijn. We kiezen bewust welke waarden nuttig zijn voor de demo, zodat de applicatie bruikbaar blijft zonder te complex te worden. | joost | `ansible/playbooks/*/info.yml`, `templates/dashboard.html` | Done |
| PB-80 | Deployment log timestamps in Belgische tijd tonen | Het tijdstip bij Laatste configuratie en de loggeschiedenis moet overeenkomen met Belgische tijd. Nu gebruikt SQLite standaard UTC, terwijl backups al Belgische tijd gebruiken. | lina | `modules/database_tools.py`, `templates/dashboard.html` | Done |
| PB-81 | Configuratiegeschiedenis tonen op dashboard | We tonen niet alleen de laatste run, maar ook een lijst met eerdere configuraties. Zo kan de docent zien wat er al gebeurd is. | Lina | `templates/dashboard.html`, `modules/database_tools.py`, `app.py` | Done |
| PB-82 | Samenvatting en technische output per log bekijken | Per configuratierun moet de samenvatting zichtbaar zijn en de technische output openklapbaar blijven, zoals bij de laatste run. | Lina | `templates/dashboard.html`, `modules/database_tools.py` | Done |
| PB-92 | Backupbestanden tonen bij succesvolle configuraties | Bij een geslaagde router/switch-run tonen we welke running-config backups bestaan. Dit moet niet meteen een volledig restore-systeem zijn. | Lina | `backups/`, `templates/dashboard.html`, `modules/database_tools.py` | Done |
| PB-93 | Backupbestanden logisch ordenen | Backups worden getoond per toestel, gebruiker en datum/tijd. Zo blijft de lijst leesbaar als er meerdere configuraties zijn uitgevoerd. | Bart | `backups/`, `modules/database_tools.py`, `templates/dashboard.html` | Done |
| PB-87 | Configuratiegeschiedenis overzichtelijker maken | De geschiedenis toont per configuratierun de setup, gebruiker, tijdstip, status, samenvatting, technische output en backups. Met eenvoudige filters op setup, status en user kan de docent sneller terugvinden wat eerder uitgevoerd is. | Team | `app.py`, `templates/dashboard.html`, `static/style.css` | Done |
| PB-94 | Sprint 3 eindflow testen | Op het einde testen we de volledige flow opnieuw: login, setup kiezen, configuratie starten, output lezen, logs bekijken en backups controleren. | Team | volledige project | Done |


## Doorschuifbare taken

Deze taken zijn nuttig, maar alleen als de Sprint 3-kern klaar is.

| PB-ID | Taak | Wat betekent dit concreet? | Eigenaar | Bestand(en) | Status |
| --- | --- | --- | --- | --- | --- |
| PB-88 | Backupbestanden downloadbaar maken | Als er tijd is, kan de gebruiker backupbestanden via de frontend downloaden. Dit is handig, maar niet verplicht voor de MVP. | Lina + Bart | `templates/dashboard.html`, `app.py`, `backups/` | Done |


## Daily stand-ups

We plannen opnieuw 4 korte momenten via MS Teams. De focus ligt deze sprint vooral op de MVP echt afwerken en zorgen dat alles duidelijk genoeg is voor een demo.

**27/05 Woensdag daily 1 | 20:00 | MS Teams**

Bart
Ik heb vooral gekeken hoe we setup2 best kunnen opbouwen volgens het labo in Brussel. Setup1 werkt al als basisopstelling, maar voor setup2 moeten we een podverhaal maken met een router, podswitches, distributieswitch en classroomswitch. Mijn volgende stap is de EVE-NG-opstelling voorbereiden en bekijken welke management-IP's en inventories nodig zijn. Ik zit nog niet echt vast, maar we moeten opletten dat setup2 niet te groot wordt.

Lina
Lina heeft gekeken naar de frontend en de geschiedenis van configuraties. De laatste configuratie wordt al getoond, maar voor Sprint 3 moet het duidelijker worden welke runs eerder gedaan zijn en welke output daarbij hoort. Haar volgende stap is de geschiedenis visueel beter tonen. Ze moet wel rekening houden met de data die Joost uit SQLite haalt.

Joost
Joost heeft verder gekeken naar de setupwaarden en hoe die op het dashboard getoond kunnen worden. Nu staan sommige waarden nog te technisch of als ruwe lijst. Zijn volgende stap is bekijken hoe we daar een eenvoudiger formulier van maken. Het belangrijkste aandachtspunt is dat de waarden niet zomaar fout in Ansible terechtkomen.

**28/05 Donderdag daily 2 | 20:00 | MS Teams**

Bart
Ik heb setup2 verder voorbereid met een eigen setupmap, eigen `info.yml` en eigen `inventory.ini`. Daardoor kan setup2 andere management-IP's gebruiken dan setup1. Mijn volgende stap is de router- en switchplaybooks van setup2 testen op de EVE-NG-toestellen. Waar ik rekening mee moet houden, is dat alle toestellen eerst een basisconfiguratie voor SSH nodig hebben.

Lina
Lina heeft verder gewerkt aan het dashboardgedeelte rond logs en output. De bedoeling is dat de docent niet alleen de laatste run ziet, maar ook eerdere configuraties kan openklappen. Haar volgende stap is de samenvatting en technische output per log duidelijk tonen. Er moest nog afgestemd worden hoe backups aan de juiste configuratierun gekoppeld worden.

Joost
Joost heeft verder gekeken naar de formulierwaarden voor de setups. De bedoeling is dat de docent nuttige waarden kan aanpassen, maar dat de applicatie nog steeds veilig blijft. Zijn volgende stap is de validatie op die invoer voorzien. Er moest nog beslist worden of aangepaste waarden tijdelijk gebruikt worden of echt in `info.yml` terechtkomen.

**29/05 Vrijdag daily 3 | 20:00 | MS Teams**

Bart
Ik heb setup2 getest en bijgestuurd. De router krijgt subinterfaces voor VLAN 10 en VLAN 20, en de switches krijgen VLANs, trunks, EtherChannel en een accesspoort aan de classroomkant. Mijn volgende stap is controleren of de backups en technische documentatie per setup kloppen. Waar ik even tegenaan liep, was dat de router wel pingbaar was maar SSH niet altijd goed reageerde tot de basisconfiguratie juist stond.

Lina
Lina heeft de configuratiegeschiedenis verder uitgewerkt. Per run kunnen we nu zien welke setup gestart werd, door welke user, met welke status en welke output erbij hoort. Haar volgende stap is ervoor zorgen dat succesvolle runs ook de backupbestanden tonen. De grootste uitdaging is dat de geschiedenis overzichtelijk moet blijven zonder een te groot admin-dashboard te bouwen.

Joost
Joost heeft het formulier voor setupwaarden verder uitgewerkt. De waarden worden niet meer als ruwe arrays getoond, maar in duidelijkere groepen. Zijn volgende stap is zorgen dat aangepaste waarden ook effectief gebruikt worden door Ansible. We hebben beslist dat waarden eerst gevalideerd worden en daarna in `info.yml` worden opgeslagen.

**30/05 Zaterdag daily 4 | 20:00 | MS Teams**

Bart
Ik heb de laatste technische stukken nagekeken: setup2 werkt met eigen inventory, de algemene inventory-fallback is weggehaald en de geschiedenis kan gefilterd worden op setup en status. Mijn volgende stap is de Sprint 3-documenten afronden en alles klaarmaken voor Sprint 4. Voor Sprint 3 zit ik niet meer echt vast, alleen de einddocumentatie moet nog verder in Sprint 4.

Lina
Lina heeft de frontend nog verder nagekeken zodat de geschiedenis, output en backups bruikbaar zijn voor een demo. De docent kan nu beter volgen wat er gebeurd is na een configuratiepush. Haar volgende stap is in Sprint 4 vooral netwerkschema uitbreiden met details (interfaces, IP-addresses), documentatie en testbewijs mee helpen verzamelen. Er zijn geen grote blokkades meer.
 
Joost
Joost heeft de validatie en de setupformulieren mee nagekeken. Foute invoer wordt tegengehouden en correcte waarden worden opgeslagen zodat Ansible ze nadien gebruikt. Zijn volgende stap is in Sprint 4 de databasewerking en de code nog goed documenteren. Er zijn geen grote blokkades meer.

Tijdens elke daily bespreken we:

- wat heb ik gedaan?
- wat ga ik nu doen?
- waar zit ik vast?


## Werkende sprintversie

Op het einde van Sprint 3 moet dit werken of duidelijk aantoonbaar zijn:

- setup1 en setup2 staan in de applicatie;
- setup2 sluit aan bij het labo/pod-verhaal uit Brussel;
- elke setup heeft eigen setupinformatie;
- elke setup kan eigen inventorygegevens gebruiken;
- variabelen worden duidelijker en mooier getoond;
- foute invoer wordt tegengehouden of duidelijk gemeld;
- configuratiegeschiedenis is zichtbaar;
- samenvatting en technische output zijn per run te bekijken;
- backups zijn zichtbaar en logisch geordend;
- Belgische tijd wordt duidelijker gebruikt bij logs;
- de volledige flow is getest;
