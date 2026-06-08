# Presentatie- en demo-stappenplan

Dit document is bedoeld als voorbereiding voor de presentatie en demo. Het volgt bewust dezelfde grote volgorde als het technisch document, zodat de docenten kunnen meevolgen in de documentatie. We lezen het technisch document niet letterlijk voor. We gebruiken het als kapstok.

De belangrijkste keuze voor de presentatie is:

```text
Eerst tonen dat de applicatie werkt, daarna uitleggen hoe alles technisch opgebouwd is.
```

Zo ziet de docent eerst het resultaat. Daarna is de uitleg over Flask, SQLite, Ansible, Docker en de netwerkopstellingen veel logischer.


## 1. Algemene presentatieflow

| Volgorde | Onderdeel | Wie | Hoofdstuk technisch document | Doel |
| --- | --- | --- | --- | --- |
| 1 | MVP intro en afbakening | Joost | Hoofdstuk 1 | Duidelijk maken wat gebouwd is, wat binnen de MVP zit en wat bewust niet. |
| 2 | Architectuur en live demo | Lina | Hoofdstuk 2 en 5.3 | Eerst tonen hoe de applicatie werkt vanuit de frontend. |
| 3 | Setup 1 uitleg | Bart | Hoofdstuk 3 | Basisopstelling uitleggen: router, switch, servers en Docker Compose. |
| 4 | Setup 2 uitleg | Lina | Hoofdstuk 4 | Podopstelling Brussel uitleggen aan de hand van het schema. |
| 5 | SQLite en logging | Joost | Hoofdstuk 6 | Uitleggen hoe users, setups, logs, output en backups bijgehouden worden. |
| 6 | Ansible-flow | Bart | Hoofdstuk 7 | Uitleggen hoe Flask via Ansible de toestellen configureert. |
| 7 | Projectverloop | Lina | Hoofdstuk 10, bijlage A | Uitleggen hoe we als team gewerkt hebben met hoofddomeinen en afspraken. |
| 8 | Scrumwerking | Bart | Hoofdstuk 10, bijlage B | Uitleggen hoe backlog, sprints, stand-ups en retrospectives gebruikt zijn. |
| 9 | Logboeken | Joost | Hoofdstuk 10, bijlage C | Uitleggen hoe changelogs en AI-logboeken gebruikt zijn als verantwoording. |

Richttijd: ongeveer 30 tot 40 minuten, afhankelijk van hoeveel vragen er tussendoor komen.


## 2. Joost - Hoofdstuk 1: MVP intro en MVP-afbakening

### Wat Joost moet duidelijk maken

Joost start de presentatie met het algemene verhaal. Het doel is dat de docent meteen begrijpt wat het project doet en waar de grens van de MVP ligt.

### Kernboodschap

```text
We hebben een netwerkbeheer-dashboard gebouwd waarmee een docent labo-opstellingen kan starten, opvolgen en controleren. De applicatie draait in Docker op een Debian-host. Via Flask kiest de docent een opstelling. Flask start daarna Ansible, en Ansible configureert de netwerktoestellen. De serverdiensten HTTP, HTTPS en FTP draaien als Docker-containers. Elke configuratierun wordt opgeslagen in SQLite, samen met output en backups.
```

### Punten die zeker gezegd moeten worden

- Dit project is een MVP, dus we focussen op een werkende kernflow.
- De kernflow is: login, opstelling kiezen, waarden bekijken of aanpassen, configuratie starten, output bekijken, geschiedenis raadplegen en backups downloaden.
- Setup 1 is de basisopstelling met 1 router, 1 switch en serverdiensten.
- Setup 2 is de podopstelling die het labo in Brussel vereenvoudigd nabootst.
- We hebben extra functionaliteit voorzien omdat dit nuttig is voor de demo: aanpasbare setupwaarden, configuratiegeschiedenis, filters en backupkoppeling.
- We hebben bewust geen onbeperkte setup-builder gemaakt. Dat zou buiten de MVP vallen en veel meer validatie en playbookgeneratie vragen.

### Wat tonen

- Hoofdstuk 1 van het technisch document.
- MVP-afbakening: wat zit erin, wat zit er niet in en waarom.

### Mogelijke zin om af te sluiten

```text
Na deze afbakening tonen we eerst de applicatie zelf. Dan is het duidelijker waarom de code en infrastructuur zo opgebouwd zijn.
```


## 3. Lina - Hoofdstuk 2 en 5.3: Architectuur en live demo

### Wat Lina moet duidelijk maken

Lina toont eerst hoe de applicatie gebruikt wordt. De focus ligt hier op de frontend en de algemene werking, niet op elk technisch detail.

### Architectuur in mensentaal

```text
De docent werkt in de browser. Flask toont het dashboard en verwerkt de acties. SQLite bewaart gebruikers, setupinformatie en configuratielogs. Ansible voert de netwerkconfiguratie uit. Docker Compose beheert de Flask-container en de servercontainers.
```

### Demo-volgorde

1. Naar de Flask-app gaan.
2. Inloggen als docent.
3. Dashboard tonen.
4. Setup 1 en setup 2 kort tonen.
5. Technische documentatie per setup openklappen.
6. Aanpasbare waarden tonen.
7. Setup 1 starten.
8. Loading/status tonen.
9. Na afloop de samenvatting tonen.
10. Technische output openklappen.
11. Geschiedenis tonen.
12. Een succesvolle run openklappen en backups tonen.

### Wat erbij gezegd wordt

```text
Op het dashboard ziet de docent welke opstellingen beschikbaar zijn. Per opstelling tonen we wat er technisch nodig is: management-IP's, interfaces, VLANs en wat de setup configureert. De belangrijkste waarden kunnen aangepast worden, maar de configuratie wordt pas echt uitgevoerd wanneer de docent op Start configuratie klikt.
```

### Koppeling met `app.py`

Lina verwijst kort naar de routes in `app.py`. Niet lijn per lijn overlopen, maar de flow uitleggen.

| Route / onderdeel | Wat zeggen |
| --- | --- |
| Loginroute | Controleert de gebruiker en start een sessie. |
| Dashboardroute | Haalt setups, laatste run en geschiedenis op. |
| Deployroute | Start de gekozen setup via de Ansible-helper. |
| Update setupwaarden | Controleert de ingevoerde waarden en schrijft ze pas daarna weg. |
| Backupdownload | Laat backups downloaden die bij een run horen. |

### Belangrijk voor Lina

- Niet te diep in Ansible gaan, dat neemt Bart later op.
- Niet te diep in database_tools gaan, dat neemt Joost later op.
- De frontend uitleggen als gebruikservaring voor de docent.


## 4. Bart - Hoofdstuk 3: Setup 1 basisopstelling

### Wat Bart moet duidelijk maken

Setup 1 is de eenvoudige basisopstelling waarmee we aantonen dat de volledige keten werkt: router, switch, servers, Ansible, Docker en backups.

### Kernboodschap

```text
Setup 1 configureert 1 router, 1 switch en 3 serverdiensten. De basisconfiguratie op de router en switch dient alleen om SSH mogelijk te maken. De echte labo-configuratie gebeurt daarna via Ansible.
```

### Wat setup 1 configureert

- Router R1:
  - hostname;
  - labinterface;
  - IP-adres op de labinterface;
  - OSPF-basisconfiguratie;
  - backup van de running-config.
- Switch SW1:
  - hostname;
  - VLAN 10 en VLAN 20;
  - accesspoort;
  - trunkpoort;
  - backup van de running-config.
- Servers:
  - HTTP-container;
  - HTTPS-container met self-signed certificaat;
  - FTP-container met gebruiker en testbestand;
  - checks of de diensten bereikbaar zijn.

### Wat tonen

- `ansible/playbooks/setup1/info.yml`
- `ansible/playbooks/setup1/router.yml`
- `ansible/playbooks/setup1/switch.yml`
- `ansible/playbooks/setup1/servers.yml`
- `docker-compose.yml`
- eventueel de backupmap van een succesvolle run

### EVE-NG aansluiting die erbij hoort

```text
MGMT-cloud -> R1 Gi0/0
MGMT-cloud -> SW1 Gi0/0
R1 Gi0/1 -> SW1 Gi0/1
SW1 Gi0/2 -> accesspoort voor VLAN 10
```

### Wat zeggen over Docker Compose

```text
Docker Compose start de Flask-container en de servercontainers. De Flask-container is de centrale applicatie. De HTTP-, HTTPS- en FTP-containers zijn de serverdiensten die door het serverplaybook gestart en gecontroleerd worden.
```

### Belangrijk voor Bart

- Duidelijk zeggen dat management en labconfiguratie gescheiden zijn.
- Duidelijk zeggen dat `info.yml` de waarden bevat die frontend en playbooks gebruiken.
- Duidelijk zeggen dat backups bewijs leveren van de configuratie.


## 5. Lina - Hoofdstuk 4: Setup 2 podopstelling Brussel

### Wat Lina moet duidelijk maken

Setup 2 is afgestemd op het labo/pod-verhaal uit de opgave. We configureren niet het volledige rack met 4 pods, maar 1 pod als duidelijk bewijs van het concept.

### Kernboodschap

```text
Setup 2 stelt 1 pod voor uit het labo in Brussel. De bedoeling is dat VLANs vanuit de pod via de distributieswitch tot aan de classroomswitch beschikbaar worden gemaakt. Zo kan de student aan de classroomkant werken terwijl de toestellen fysiek aan de podkant staan.
```

### Wat setup 2 configureert

- R1:
  - router-on-a-stick;
  - subinterfaces per VLAN;
  - gateway-IP's voor de VLANs.
- SW11 en SW12:
  - VLANs;
  - trunklinks tussen router, podswitches en distributieswitch.
- DISTSW:
  - VLANs;
  - trunk naar SW12;
  - EtherChannel richting CLASSSW.
- CLASSSW:
  - VLANs;
  - EtherChannel richting DISTSW;
  - accesspoorten voor de classroomkant.

### Wat tonen

- Setup 2 diagram.
- `ansible/playbooks/setup2/info.yml`
- eventueel de technische documentatie op het dashboard.
- eventueel een succesvolle running-config backup.

### Belangrijk om te zeggen

```text
In de echte opgave spreekt men over meerdere pods. Voor de MVP tonen we het principe met 1 pod. Dat maakt de demo haalbaar, maar toont wel de belangrijkste technische onderdelen: VLANs, trunks, router-on-a-stick en EtherChannel.
```


## 6. Joost - Hoofdstuk 6: SQLite en database

### Wat Joost moet duidelijk maken

Joost legt uit hoe de applicatie gegevens bewaart. De focus ligt op gebruikers, setups, configuratieruns, output en backups.

### Kernboodschap

```text
SQLite is gekozen omdat dit voor een MVP eenvoudig, lokaal en reproduceerbaar is. We hebben geen aparte databaseserver nodig. De database bewaart gebruikers, beschikbare setups en alle configuratieruns.
```

### Wat zeker aan bod komt

- `users`: gebruikers van de applicatie.
- Wachtwoorden worden gehasht opgeslagen.
- `network_setups`: welke opstellingen bestaan.
- `deployment_logs`: elke configuratierun met user, setup, timestamp, status, output en run reference.
- Geschiedenisfilters gebruiken de data uit SQLite.
- Backups worden via `run_reference` gekoppeld aan de juiste run.

### Wat tonen

- `database/schema.sql`
- `modules/database_tools.py`
- dashboardgeschiedenis

### Belangrijk voor Joost

- Niet alleen tabellen noemen, maar uitleggen waarom ze nodig zijn.
- Duidelijk maken dat geschiedenis en backups niet los staan van elkaar.
- Duidelijk maken dat SQLite voldoende is voor deze MVP.


## 7. Bart - Hoofdstuk 7: Ansible-flow

### Wat Bart moet duidelijk maken

Bart legt uit hoe Flask niet zelf Cisco-commando's uitvoert, maar Ansible aanstuurt.

### Kernboodschap

```text
Ansible is de laag die echt met de Cisco-toestellen praat. Flask vraagt aan onze Ansible-helper om een setup uit te voeren. Die helper kiest de juiste setupmap, maakt de juiste inventory, start de playbooks en geeft de output terug aan Flask.
```

### `ansible_tools.py` uitleg in stappen

1. Flask roept `run_setup(setup_id)` aan.
2. De helper zoekt de juiste setupmap.
3. De helper leest de setupinformatie.
4. De helper maakt of gebruikt de juiste inventory.
5. De helper start de playbooks in volgorde.
6. Ansible-output wordt opgevangen.
7. Er wordt een eenvoudige samenvatting gemaakt.
8. De volledige output gaat terug naar Flask.
9. Flask slaat de run op in SQLite.
10. Backups worden per run gekoppeld via `run_reference`.

### Inventory uitleg

```text
De inventory zegt aan Ansible welke toestellen bestaan en hoe Ansible ermee moet verbinden. We gebruiken per setup een eigen inventory, omdat setup 1 en setup 2 andere toestellen en management-IP's kunnen hebben.
```

### Belangrijke inventory-instellingen

- `network_cli`: Ansible gebruikt netwerkcommando's in plaats van gewone Linux-SSH.
- `cisco.ios.ios`: de toestellen zijn Cisco IOS-toestellen.
- `paramiko`: SSH-methode die stabiel werkte met onze EVE-NG Cisco IOSv-images.
- timeouts: nodig omdat geemuleerde toestellen soms traag reageren.
- SSH common args: nodig omdat oudere Cisco IOSv-images oudere SSH-algoritmes gebruiken.

### Output uitleg

```text
De technische output komt van Ansible zelf. Onze applicatie voegt daarboven een eenvoudige samenvatting toe. Zo ziet de docent snel wat gelukt of gefaald is, maar blijft de volledige technische output beschikbaar.
```


## 8. Lina - Hoofdstuk 10, bijlage A: Projectverloop

### Wat Lina moet duidelijk maken

Lina legt uit hoe we het project georganiseerd hebben zodat iedereen apart kon werken, maar het project toch een geheel bleef.

### Kernboodschap

```text
We hebben bewust met hoofddomeinen gewerkt. Lina focuste vooral op Flask en frontend, Joost op SQLite en backend, Bart op Ansible, Docker en netwerk. Door duidelijke koppelafspraken konden die onderdelen samen blijven werken.
```

### Wat zeker gezegd wordt

- Iedereen had een hoofddomein.
- Iedereen moest wel globaal begrijpen hoe het geheel werkte.
- Koppelafspraken waren belangrijk om conflicten te vermijden.
- Voorbeelden van koppelafspraken:
  - `run_setup()` geeft altijd status en output terug;
  - statuswaarden zijn `success` of `failed`;
  - setupdata komt uit `info.yml`;
  - logs worden in SQLite bewaard;
  - backups worden per runmap bewaard.


## 9. Bart - Hoofdstuk 10, bijlage B: Scrumwerking

### Wat Bart moet duidelijk maken

Bart legt uit hoe we Scrum praktisch hebben toegepast.

### Kernboodschap

```text
We hebben gewerkt met een product backlog, sprintdocumenten, stand-ups en retrospectives. Per sprint bepaalden we een doel, kozen we taken uit de backlog en evalueerden we nadien wat goed ging en wat beter moest.
```

### Wat zeker gezegd wordt

- Sprint 1: basisstructuur, eerste Flask/SQLite/Docker/Ansible-basis.
- Sprint 2: basisopstelling technisch werkend maken.
- Sprint 3: MVP bruikbaar afwerken, setup 2 toevoegen, geschiedenis en variabelen verbeteren.
- Sprint 4: documentatie, demo, code-uitleg en afwerking.
- Stand-ups werden gebruikt om kort op te volgen wat gedaan was, wat gepland was en waar iemand vastzat.
- Retrospectives werden gebruikt om leerpunten mee te nemen naar de volgende sprint.

### Wat tonen

- `docs/scrum/product-backlog.md`
- `docs/scrum/sprint-1.md` tot `sprint-4.md`
- retrospectives


## 10. Joost - Hoofdstuk 10, bijlage C: Logboeken

### Wat Joost moet duidelijk maken

Joost sluit het projectverloop af met de persoonlijke logboeken en changelogs.

### Kernboodschap

```text
Naast de Scrumdocumenten hebben we persoonlijke changelogs en AI-logboeken bijgehouden. Daarmee tonen we wie waaraan gewerkt heeft, welke problemen besproken zijn en hoe AI gebruikt werd als ondersteuning.
```

### Wat zeker gezegd wordt

- Changelogs tonen welke technische aanpassingen per persoon gebeurden.
- AI-logboeken tonen welke vragen, problemen of keuzes met AI besproken werden.
- De logboeken zijn bedoeld als verantwoording, niet als vervanging van eigen kennis.
- Iedereen moet zijn eigen wijzigingen kunnen uitleggen.





## 12. Demo fallback

Als de live demo faalt door EVE-NG, VPN, hotspot, SSH of een gepauzeerde VM, gebruiken we dit als fallback.

### Stappen

1. Toon de foutmelding in de applicatie.
2. Leg uit dat fouten bewust gelogd worden.
3. Toon de technische output.
4. Toon een vorige succesvolle run in de geschiedenis.
5. Toon de backups van die succesvolle run.
6. Toon eventueel de running-config bewijsbestanden.

### Wat zeggen

```text
Omdat we met geemuleerde hardware, VPN en een labo-omgeving werken, kan bereikbaarheid soms falen. Dat is net waarom we output, geschiedenis en backups bewaren. Zelfs bij een fout kunnen we aantonen waar het misloopt.
```


## 13. Afsluiting

### Wie

Team samen, kort.

### Afsluitende boodschap

```text
Samengevat hebben we een werkende MVP gebouwd waarmee een docent netwerkopstellingen kan starten via een webdashboard. Flask verzorgt de interface, SQLite bewaart gebruikers en logs, Ansible configureert de netwerktoestellen en Docker Compose beheert de applicatie en servercontainers. De geschiedenis en backups zorgen ervoor dat elke configuratierun achteraf controleerbaar blijft.
```

### Laatste punt

```text
De MVP is bewust beperkt, maar de volledige kernflow uit de opgave is aanwezig en reproduceerbaar gedocumenteerd en dat was voor ons de essentie..
```
