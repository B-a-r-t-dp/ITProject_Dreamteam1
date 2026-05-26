# Setup2 - Podopstelling Brussel

Deze map bevat de Ansible-bestanden voor de tweede netwerkopstelling.

Setup2 stelt 1 werkende pod voor uit het labo in Brussel. De volledige opgave
spreekt over 4 pods, maar voor onze MVP configureren we 1 pod volledig. Hetzelfde
principe kan later herhaald worden voor de andere pods.

## EVE-NG aansluitingen

We gebruiken 2 soorten verbindingen:

- managementverbindingen voor SSH en Ansible;
- labo/opgaveverbindingen voor VLANs, trunks en EtherChannel.

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

De 2 links tussen `DIST-SW` en `CLASS-SW` worden door Ansible als
EtherChannel trunk geconfigureerd.

## Management-IP's

```text
R1       192.168.0.221
SW-1-1   192.168.0.222
SW-1-2   192.168.0.223
DIST-SW  192.168.0.224
CLASS-SW 192.168.0.225
```

## Startup-configs voor SSH

Deze startup-configs dienen alleen om de toestellen bereikbaar te maken via SSH.
De echte opgaveconfiguratie gebeurt daarna via Ansible.

### R1

```cisco
hostname R1
no service config
no ip domain lookup
ip domain name itproject.local
enable secret azerty
username admin privilege 15 secret azerty

default interface GigabitEthernet0/1

interface GigabitEthernet0/1
 description Management voor SSH en Ansible
 ip address 192.168.0.221 255.255.255.0
 no shutdown

ip ssh version 2
crypto key generate rsa modulus 1024

line vty 0 4
 login local
 transport input ssh
 privilege level 15
 exec-timeout 30 0

end
```

### SW-1-1

```cisco
hostname SW11
no service config
no ip domain lookup
ip domain name itproject.local
enable secret azerty
username admin privilege 15 secret azerty

interface Vlan1
 description Management voor SSH en Ansible
 no ip address dhcp
 no ip address
 ip address 192.168.0.222 255.255.255.0
 no shutdown

ip default-gateway 192.168.0.1
ip ssh version 2
crypto key generate rsa modulus 1024

line vty 0 4
 login local
 transport input ssh
 privilege level 15
 exec-timeout 30 0

end
```

### SW-1-2

```cisco
hostname SW12
no service config
no ip domain lookup
ip domain name itproject.local
enable secret azerty
username admin privilege 15 secret azerty

interface Vlan1
 description Management voor SSH en Ansible
 no ip address dhcp
 no ip address
 ip address 192.168.0.223 255.255.255.0
 no shutdown

ip default-gateway 192.168.0.1
ip ssh version 2
crypto key generate rsa modulus 1024

line vty 0 4
 login local
 transport input ssh
 privilege level 15
 exec-timeout 30 0

end
```

### DIST-SW

```cisco
hostname DISTSW
no service config
no ip domain lookup
ip domain name itproject.local
enable secret azerty
username admin privilege 15 secret azerty

interface Vlan1
 description Management voor SSH en Ansible
 no ip address dhcp
 no ip address
 ip address 192.168.0.224 255.255.255.0
 no shutdown

ip default-gateway 192.168.0.1
ip ssh version 2
crypto key generate rsa modulus 1024

line vty 0 4
 login local
 transport input ssh
 privilege level 15
 exec-timeout 30 0

end
```

### CLASS-SW

```cisco
hostname CLASSSW
no service config
no ip domain lookup
ip domain name itproject.local
enable secret azerty
username admin privilege 15 secret azerty

interface Vlan1
 description Management voor SSH en Ansible
 no ip address dhcp
 no ip address
 ip address 192.168.0.225 255.255.255.0
 no shutdown

ip default-gateway 192.168.0.1
ip ssh version 2
crypto key generate rsa modulus 1024

line vty 0 4
 login local
 transport input ssh
 privilege level 15
 exec-timeout 30 0

end
```

## Controlecommando's

Router:

```cisco
show ip interface brief
show running-config interface GigabitEthernet0/0
show running-config interface GigabitEthernet0/0.10
show running-config interface GigabitEthernet0/0.20
```

Switches:

```cisco
show vlan brief
show interfaces trunk
```

Alleen op `DIST-SW` en `CLASS-SW`:

```cisco
show etherchannel summary
```
