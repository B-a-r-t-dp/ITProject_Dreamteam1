# Setup1 - Basisopstelling

Deze map bevat de Ansible-bestanden voor de eerste netwerkopstelling.

Setup1 is de basis-MVP:

- 1 router;
- 1 switch;
- HTTP-container;
- HTTPS-container;
- FTP-container.

## Bestanden

```text
inventory.ini  -> toestellen en SSH-gegevens voor setup1
info.yml       -> centrale waarden die de playbooks gebruiken
router.yml     -> configuratie van R1
switch.yml     -> configuratie van SW1
servers.yml    -> starten en controleren van HTTP, HTTPS en FTP
```

## Management-IP's

```text
R1  192.168.0.215
SW1 192.168.0.216
```

Deze IP's worden gebruikt door Ansible om via SSH te verbinden.

## Wat configureert Ansible?

### Router

R1 krijgt:

- hostname `R1`;
- labinterface `Gi0/1`;
- IP-adres `192.168.10.1/24`;
- eenvoudige OSPF-basis.

### Switch

SW1 krijgt:

- hostname `SW1`;
- VLAN 10 `DOCENTEN`;
- VLAN 20 `STUDENTEN`;
- accesspoort `Gi0/2` voor VLAN 10;
- trunkpoort `Gi0/3` voor VLAN 10 en VLAN 20.

### Servers

Het serverplaybook start en controleert:

- HTTP op poort 80;
- HTTPS op poort 443;
- FTP op poort 20/21 en passive poorten 30000-30010.

## Belangrijk

De startup-config in EVE-NG dient alleen om SSH en management klaar te zetten.
De echte configuratie gebeurt via deze Ansible-playbooks.

## Controlecommando's

Router:

```cisco
show ip interface brief
show running-config interface GigabitEthernet0/1
show running-config | section router ospf
```

Switch:

```cisco
show vlan brief
show running-config interface GigabitEthernet0/2
show running-config interface GigabitEthernet0/3
show interfaces trunk
```
