# Setup2 - Technische documentatie podopstelling Brussel

## Doel van deze opstelling

Setup2 is gebaseerd op het labo-podscenario uit de opdracht en op de uitleg van
het labo in Brussel.

De opdracht spreekt over pods achter een glazen wand. Studenten zitten in een
klaslokaal en configureren de toestellen niet rechtstreeks aan het rack. De
poorten van de pod moeten daarom via switches beschikbaar gemaakt worden in het
klaslokaal.

Voor onze MVP configureren we 1 representatieve pod volledig. De volledige
opdracht spreekt over 4 pods, maar dat zou voor Sprint 3 te groot worden om
duidelijk te testen en uit te leggen. Hetzelfde principe kan later herhaald
worden voor pod 2, pod 3 en pod 4.

## Waarom 1 pod?

Een volledige rackopstelling zou bestaan uit:

- 4 routers;
- 8 pod-switches;
- 1 distributieswitch;
- 1 classroomswitch.

Dat zijn veel toestellen voor een MVP-demo. Daarom tonen we visueel het idee van
4 pods, maar configureren we technisch 1 pod volledig.

Onze keuze is dus:

```text
1 werkende pod = bewijs dat het principe werkt
```

## Logische opbouw

De werkende pod is opgebouwd als:

```text
R1 -> SW11 -> SW12 -> DISTSW == CLASSSW
```

Betekenis:

- `R1`: router van pod 1;
- `SW11`: eerste switch van pod 1;
- `SW12`: tweede switch van pod 1;
- `DISTSW`: distributieswitch aan de pod/serverruimte-kant;
- `CLASSSW`: classroomswitch aan de klaslokaal-kant.

Tussen `DISTSW` en `CLASSSW` liggen 2 fysieke verbindingen. Die worden via
EtherChannel logisch als 1 verbinding gebruikt. Over die verbinding lopen VLAN
10 en VLAN 20 via trunk.

## EVE-NG aansluitingen

We maken bewust een verschil tussen management en de echte labo-opstelling.

Management wordt alleen gebruikt voor SSH en Ansible. De labo-opstelling wordt
gebruikt voor VLANs, trunks en EtherChannel.

### Managementverbindingen

```text
MGMT -> R1       Gi0/1
MGMT -> SW-1-1   Gi0/0
MGMT -> SW-1-2   Gi0/0
MGMT -> DIST-SW  Gi0/0
MGMT -> CLASS-SW Gi0/0
```

### Labo/opgaveverbindingen

```text
R1 Gi0/0        -> SW-1-1 Gi0/1
SW-1-1 Gi0/2    -> SW-1-2 Gi0/1
SW-1-2 Gi0/2    -> DIST-SW Gi0/1

DIST-SW Gi0/2   -> CLASS-SW Gi0/1
DIST-SW Gi0/3   -> CLASS-SW Gi0/2
```

De 2 links tussen `DIST-SW` en `CLASS-SW` stellen de verbinding tussen de
pod/serverruimte-kant en de klaslokaal-kant voor.

## Management-IP-adressen

Elke actieve node heeft een eigen management-IP. Deze IP-adressen worden gebruikt
door Ansible om via SSH verbinding te maken.

```text
R1       192.168.0.221
SW-1-1   192.168.0.222
SW-1-2   192.168.0.223
DIST-SW  192.168.0.224
CLASS-SW 192.168.0.225
```

Deze waarden staan ook in:

```text
ansible/playbooks/setup2/inventory.ini
ansible/playbooks/setup2/info.yml
```

## VLAN-plan

Voor setup2 gebruiken we 2 VLANs:

| VLAN | Naam | Doel |
| --- | --- | --- |
| 10 | DOCENTEN | eerste logisch netwerk binnen de pod |
| 20 | STUDENTEN | tweede logisch netwerk binnen de pod |

Beide VLANs worden over de trunks vervoerd van de pod naar de classroomswitch.

## Routerconfiguratie

R1 gebruikt router-on-a-stick.

De fysieke interface `Gi0/0` heeft zelf geen IP-adres. Daarop worden
subinterfaces gemaakt:

```text
Gi0/0.10 -> VLAN 10 -> 192.168.10.1/24
Gi0/0.20 -> VLAN 20 -> 192.168.20.1/24
```

Hierdoor kan R1 later routing doen tussen VLAN 10 en VLAN 20.

De managementinterface van R1 is:

```text
Gi0/1 -> 192.168.0.221/24
```

## Switchconfiguratie

### SW11

SW11 is de eerste pod-switch.

Belangrijke poorten:

```text
Gi0/1 -> trunk naar R1
Gi0/2 -> trunk naar SW12
```

Beide trunks laten VLAN 10 en VLAN 20 toe.

### SW12

SW12 is de tweede pod-switch.

Belangrijke poorten:

```text
Gi0/1 -> trunk naar SW11
Gi0/2 -> trunk naar DISTSW
```

Ook hier lopen VLAN 10 en VLAN 20 over de trunk.

### DISTSW

DISTSW is de switch aan de pod/serverruimte-kant.

Belangrijke poorten:

```text
Gi0/1 -> trunk naar SW12
Gi0/2 -> EtherChannel link 1 naar CLASSSW
Gi0/3 -> EtherChannel link 2 naar CLASSSW
```

`Gi0/2` en `Gi0/3` vormen samen:

```text
Port-channel1
```

Die port-channel is een trunk voor VLAN 10 en VLAN 20.

### CLASSSW

CLASSSW is de switch aan de klaslokaal-kant.

Belangrijke poorten:

```text
Gi0/1 -> EtherChannel link 1 naar DISTSW
Gi0/2 -> EtherChannel link 2 naar DISTSW
Gi0/3 -> studentpoort VLAN 10
```

De studentpoort stelt een poort aan de tafel in het klaslokaal voor.

## Wat gebeurt via startup-config?

De startup-config in EVE-NG gebruiken we alleen om de toestellen bereikbaar te
maken.

Daarin staat:

- hostname;
- management-IP;
- admin-gebruiker;
- SSH;
- VTY-login.

De eigenlijke opdrachtconfiguratie zetten we niet handmatig in de startup-config.
Die gebeurt via onze Flask/Ansible-applicatie.

## Wat gebeurt via Ansible?

Ansible configureert de echte setup2-opdracht:

- hostnames;
- VLAN 10 en VLAN 20;
- trunks tussen de switches;
- EtherChannel tussen `DISTSW` en `CLASSSW`;
- router-subinterfaces op R1;
- accesspoort op `CLASSSW`;
- backup van de running-configs.

De technische waarden staan centraal in:

```text
ansible/playbooks/setup2/info.yml
```

De toestellen en management-IP's staan in:

```text
ansible/playbooks/setup2/inventory.ini
```

## Controlecommando's

### Router

```cisco
show ip interface brief
show running-config interface GigabitEthernet0/0
show running-config interface GigabitEthernet0/0.10
show running-config interface GigabitEthernet0/0.20
```

Wat we willen zien:

```text
Gi0/0.10 -> 192.168.10.1
Gi0/0.20 -> 192.168.20.1
Gi0/1    -> 192.168.0.221
```

### Switches

```cisco
show vlan brief
show interfaces trunk
```

Op `DISTSW` en `CLASSSW` controleren we ook:

```cisco
show etherchannel summary
```

## Resultaat van de test

Setup2 werd succesvol uitgevoerd via het dashboard.

De applicatie gaf status `success` terug voor:

- `router.yml`;
- `switch.yml`.

Daarna zijn running-config backups aangemaakt voor:

- `r1`;
- `sw11`;
- `sw12`;
- `distsw`;
- `classsw`.

Uit de backups blijkt dat de router-subinterfaces, trunks, EtherChannel en
accesspoort effectief geconfigureerd zijn.
