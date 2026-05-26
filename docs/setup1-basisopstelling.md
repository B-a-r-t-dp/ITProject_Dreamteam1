# Setup1 - Technische documentatie basisopstelling

## Doel van deze opstelling

Setup1 is de basisopstelling van onze MVP.

Deze opstelling toont dat onze Flask/Ansible-applicatie een eenvoudige
netwerk- en serverconfiguratie kan uitvoeren.

Setup1 bevat:

- 1 router;
- 1 switch;
- HTTP-container;
- HTTPS-container;
- FTP-container.

Deze setup is bewust kleiner dan setup2. Setup1 dient vooral om de volledige
flow van de applicatie te bewijzen:

```text
login -> setup kiezen -> Ansible starten -> output opslaan -> backup maken
```

## Logische opbouw

```text
R1 -> SW1
```

Daarnaast worden via Docker Compose de servercontainers gestart en gecontroleerd.

## EVE-NG aansluitingen

Setup1 gebruikt een aparte managementverbinding voor SSH en Ansible.

```text
MGMT -> R1  Gi0/0
MGMT -> SW1 Gi0/1
```

De laboverbinding gebruikt aparte interfaces:

```text
R1  Gi0/1 -> labinterface op router
SW1 Gi0/2 -> accesspoort VLAN 10
SW1 Gi0/3 -> trunkpoort VLAN 10 en VLAN 20
```

De exacte fysieke aansluiting kan in EVE-NG verschillen, maar de waarden die de
playbooks gebruiken staan centraal in:

```text
ansible/playbooks/setup1/info.yml
```

## Management-IP-adressen

```text
R1  192.168.0.215
SW1 192.168.0.216
```

Deze IP-adressen worden gebruikt door Ansible om via SSH te verbinden.

Ze staan in:

```text
ansible/playbooks/setup1/inventory.ini
ansible/playbooks/setup1/info.yml
```

## VLAN-plan

Voor setup1 gebruiken we 2 VLANs:

| VLAN | Naam | Doel |
| --- | --- | --- |
| 10 | DOCENTEN | accesspoort en trunk |
| 20 | STUDENTEN | trunk |

## Routerconfiguratie

R1 krijgt een labinterface:

```text
Gi0/1 -> 192.168.10.1/24
```

Daarnaast wordt een eenvoudige OSPF-basis geconfigureerd:

```text
router ospf 1
router-id 1.1.1.1
network 192.168.10.0 0.0.0.255 area 0
```

Deze OSPF-configuratie is beperkt, maar toont dat het routerplaybook meer doet
dan alleen een hostname zetten.

## Switchconfiguratie

SW1 krijgt:

- hostname `SW1`;
- VLAN 10 `DOCENTEN`;
- VLAN 20 `STUDENTEN`;
- accesspoort voor VLAN 10;
- trunkpoort voor VLAN 10 en VLAN 20.

Volgens `info.yml` is dat:

```text
Gi0/2 -> access VLAN 10
Gi0/3 -> trunk VLAN 10,20
```

## Serverconfiguratie

Setup1 start en controleert ook de servercontainers.

De serverdiensten zijn:

| Service | Poort | Doel |
| --- | --- | --- |
| HTTP | 80 | gewone nginx-testpagina |
| HTTPS | 443 | nginx met self-signed certificaat |
| FTP | 20/21 en passive 30000-30010 | vsftpd met testgebruiker en testbestand |

Het serverplaybook doet niet alleen debugtekst tonen. Het start de containers
via Docker Compose en controleert of de diensten bereikbaar zijn.

## Wat gebeurt via startup-config?

De startup-config in EVE-NG gebruiken we alleen om router en switch bereikbaar te
maken voor Ansible.

Daarin staat:

- hostname;
- management-IP;
- admin-gebruiker;
- SSH;
- VTY-login.

De echte setupconfiguratie gebeurt daarna via Ansible.

## Wat gebeurt via Ansible?

Ansible configureert setup1 via:

```text
ansible/playbooks/setup1/router.yml
ansible/playbooks/setup1/switch.yml
ansible/playbooks/setup1/servers.yml
```

De playbooks gebruiken waarden uit:

```text
ansible/playbooks/setup1/info.yml
```

Daardoor staan de belangrijkste waarden op 1 centrale plaats.

Ansible doet:

- routerconfiguratie;
- switchconfiguratie;
- servercontainers starten;
- HTTP/HTTPS/FTP controleren;
- running-config backups maken van router en switch.

## Controlecommando's

### Router

```cisco
show ip interface brief
show running-config interface GigabitEthernet0/1
show running-config | section router ospf
```

Wat we willen zien:

```text
Gi0/1 -> 192.168.10.1
OSPF process 1
network 192.168.10.0 0.0.0.255 area 0
```

### Switch

```cisco
show vlan brief
show running-config interface GigabitEthernet0/2
show running-config interface GigabitEthernet0/3
show interfaces trunk
```

Wat we willen zien:

```text
VLAN 10 DOCENTEN
VLAN 20 STUDENTEN
Gi0/2 access VLAN 10
Gi0/3 trunk VLAN 10,20
```

### Servers

Vanaf de host of browser:

```text
http://127.0.0.1
https://127.0.0.1
ftp://127.0.0.1
```

FTP-login:

```text
gebruiker: ftpuser
wachtwoord: itproject
```

## Resultaat van de test

Setup1 werd succesvol uitgevoerd via het dashboard.

De applicatie gaf status `success` terug voor:

- `router.yml`;
- `switch.yml`;
- `servers.yml`.

Daarna zijn running-config backups aangemaakt voor de router en switch.

Deze setup bewijst dat de volledige basisflow van het project werkt.
