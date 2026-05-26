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
| PB-83 | Tweede netwerkopstelling toevoegen volgens labo Brussel | We maken een tweede opstelling die aansluit bij het labo/pod-verhaal uit de opgave. Dit hoeft niet groter te worden dan nodig, maar moet wel duidelijk tonen hoe de tweede opstelling verschilt van setup1. | Bart | `ansible/playbooks/setup2/`, `database/`, `docs/` | To do |
| PB-84 | Inventory per netwerkopstelling voorzien | Elke setup krijgt een eigen `inventory.ini`. Zo kan setup1 bijvoorbeeld `192.168.0.215` gebruiken en setup2 andere management-IP's. De namen `r1` en `sw1` blijven dan rollen binnen die setup. | Bart | `ansible/playbooks/setup1/inventory.ini`, `ansible/playbooks/setup2/inventory.ini`, `modules/ansible_tools.py` | To do |
| PB-85 | Ansible-helper uitbreiden voor meerdere setupmappen | `run_setup()` mag niet hardcoded alleen setup1 starten. De helper moet op basis van de gekozen setup de juiste map, playbooks en inventory gebruiken. | Bart | `modules/ansible_tools.py`, `modules/database_tools.py` | To do |
| PB-86 | Dashboard meerdere opstellingen laten tonen en starten | Het dashboard moet setup1 en setup2 tonen. Elke opstelling toont haar eigen info en de startknop moet de juiste setup-id doorgeven. | Bart | `templates/dashboard.html`, `modules/database_tools.py`, `app.py` | To do |
| PB-77 | Klein formulier voorzien voor variabelen | De docent ziet de variabelen niet meer als ruwe lijst of array, maar in een duidelijk formulier of overzicht. Eerst mag dit vooral zichtbaar zijn, daarna zorgen dat de variabelen beperkt aanpasbaar zijn. | joost | `templates/dashboard.html`, `static/style.css`, `app.py` | To do |
| PB-78 | Aangepaste waarden doorgeven aan Ansible | Als een waarde aangepast wordt, moet die ook gebruikt worden door Ansible. We moeten kiezen of we dit tijdelijk doen of opslaan in database/setupdata. | Joost | `modules/database_tools.py`, `modules/ansible_tools.py`, `app.py` | To do |
| PB-79 | validatie voorzien op de variabelen. | Voor we waarden naar Ansible sturen, controleren we simpele fouten. Bijvoorbeeld geen lege hostname, VLAN-ID moet een nummer zijn, IP-adres moet er geldig uitzien. | Joost | `modules/database_tools.py`, `app.py` | To do |
| PB-91 | Alleen veilige variabelen aanpasbaar maken | Niet alles uit `info.yml` moet aanpasbaar zijn. We kiezen bewust welke waarden veilig zijn voor de demo, zodat de applicatie niet onnodig complex wordt. | joost | `ansible/playbooks/*/info.yml`, `templates/dashboard.html` | To do |
| PB-80 | Deployment log timestamps in Belgische tijd tonen | Het tijdstip bij Laatste configuratie en de loggeschiedenis moet overeenkomen met Belgische tijd. Nu gebruikt SQLite standaard UTC, terwijl backups al Belgische tijd gebruiken. | lina | `modules/database_tools.py`, `templates/dashboard.html` | To do |
| PB-81 | Configuratiegeschiedenis tonen op dashboard | We tonen niet alleen de laatste run, maar ook een lijst met eerdere configuraties. Zo kan de docent zien wat er al gebeurd is. | Lina | `templates/dashboard.html`, `modules/database_tools.py`, `app.py` | To do |
| PB-82 | Samenvatting en technische output per log bekijken | Per configuratierun moet de samenvatting zichtbaar zijn en de technische output openklapbaar blijven, zoals bij de laatste run. | Lina | `templates/dashboard.html`, `modules/database_tools.py` | To do |
| PB-92 | Backupbestanden tonen bij succesvolle configuraties | Bij een geslaagde router/switch-run tonen we welke running-config backups bestaan. Dit moet niet meteen een volledig restore-systeem zijn. | Lina | `backups/`, `templates/dashboard.html`, `modules/database_tools.py` | To do |
| PB-93 | Backupbestanden logisch ordenen | Backups worden getoond per toestel, gebruiker en datum/tijd. Zo blijft de lijst leesbaar als er meerdere configuraties zijn uitgevoerd. | Bart | `backups/`, `modules/database_tools.py`, `templates/dashboard.html` | To do |
| PB-87 | Volledige configuratieflow debuggen | We testen bewust router offline, switch offline, FTP fout, Docker-container conflict en foute input. De applicatie moet dan duidelijk genoeg tonen wat er misloopt. | Team | `app.py`, `modules/ansible_tools.py`, `templates/dashboard.html`, `docs/` | To do |
| PB-94 | Sprint 3 eindflow testen | Op het einde testen we de volledige flow opnieuw: login, setup kiezen, configuratie starten, output lezen, logs bekijken en backups controleren. | Team | volledige project | To do |


## Doorschuifbare taken

Deze taken zijn nuttig, maar alleen als de Sprint 3-kern klaar is.

| PB-ID | Taak | Wat betekent dit concreet? | Eigenaar | Bestand(en) | Status |
| --- | --- | --- | --- | --- | --- |
| PB-88 | Backupbestanden downloadbaar maken | Als er tijd is, kan de gebruiker backupbestanden via de frontend downloaden. Dit is handig, maar niet verplicht voor de MVP. | Lina + Bart | `templates/dashboard.html`, `app.py`, `backups/` | To do |
| PB-89 | Output nog verder opdelen per playbook | Als de huidige samenvatting niet genoeg is, kunnen router, switch en servers visueel apart getoond worden. Dit is extra afwerking. | Lina + Bart | `modules/ansible_tools.py`, `templates/dashboard.html` | To do |


## Daily stand-ups

| Moment | Tijdstip | Medium | Korte notities |
| --- | --- | --- | --- |
| Woensdag daily 1 | 20:00 | MS Teams |  |
| Donderdag daily 2 | 20:00 | MS Teams |  |
| Vrijdag daily 3 | 20:00 | MS Teams |  |
| Zaterdag daily 4 | 20:00 | MS Teams |  |

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
- veilige variabelen zijn waar haalbaar aanpasbaar;
- foute invoer wordt tegengehouden of duidelijk gemeld;
- configuratiegeschiedenis is zichtbaar;
- samenvatting en technische output zijn per run te bekijken;
- backups zijn zichtbaar en logisch geordend;
- Belgische tijd wordt duidelijker gebruikt bij logs;
- de volledige flow is getest;
- Sprint 4 kan focussen op documentatie, testing, screenshots en code learning.
