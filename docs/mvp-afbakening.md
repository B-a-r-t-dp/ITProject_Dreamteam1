# MVP-afbakening

## Waarom afbakenen?

De volledige opdracht is groot. Binnen de beschikbare tijd is het risico groot dat we alles half proberen te maken.

Daarom kiezen we voor een kleine, verdedigbare MVP. We tonen de kern van de opdracht en leggen eerlijk uit wat we niet bouwen.

## Wat bouwen we zeker?

| Onderdeel | MVP-uitwerking |
| --- | --- |
| Flask | Loginpagina, dashboardpagina en knop om configuratie te starten. |
| SQLite | Tabellen `users`, `network_setups`, `deployment_logs`. |
| Wachtwoorden | Niet in plaintext, maar met password hashing. |
| Ansible | Vanuit Flask startbaar via een eenvoudige helperfunctie. |
| Router | Basisplaybook voor 1 router. |
| Switch | Basisplaybook voor 1 switch. |
| HTTP | Eigen Alpine-container met eenvoudige indexpagina. |
| HTTPS | Eigen Alpine-container met eenvoudige indexpagina en TLS/SSL. |
| FTP | Eigen Alpine-container met FTP-service en testbestand. |
| Docker Compose | Bestand om containers samen te bouwen/starten. |
| Documentatie | Uitleg over opstelling, keuzes, installatie en beperkingen. |

## Wat bouwen we beperkt?

| Onderdeel | Beperking | Waarom? |
| --- | --- | --- |
| Routerconfiguratie | Alleen minimum: hostname, interface/IP, routing, OSPF-basis. | Genoeg om de vereiste te tonen. |
| Switchconfiguratie | Alleen minimum: hostname, 2 VLANs, accesspoort, trunkpoort. | Genoeg om de vereiste te tonen. |
| Netwerkopstellingen | Eerst 1 vaste opstelling. | Meerdere opstellingen maken het project groter. |
| Webinterface | Simpele pagina's, geen uitgebreide styling. | Functionaliteit is belangrijker dan uiterlijk. |
| Ansible-output | Output na uitvoering tonen, niet realtime. | Realtime output is complexer en optioneel. |

## Wat bouwen we niet in de MVP of enkel als de tijd het toelaat?

| Onderdeel | Waarom niet? |
| --- | --- |
| Adminpagina | Extra CRUD-functionaliteit is te groot voor de basis. |
| Meerdere netwerkopstellingen | Eerst 1 flow betrouwbaar maken. |
| Realtime output | Bonus, niet nodig voor de kern. |
| Uitgebreide Ansible roles | Eenvoudige playbooks zijn beter uitlegbaar. |
| CI/CD-pipeline | Bonus, geen kernvereiste voor de demo. |
| Productie-security | We doen basisveiligheid, maar geen volledig productieplatform. |
| Volledig lab in 1 keer configureren | Te groot; focus op 1 router, 1 switch en 3 servercontainers. |

## Waarom is dit verdedigbaar?

Deze MVP toont de belangrijkste flow:

```text
Docent logt in
Docent kiest 1 netwerkopstelling
Flask start Ansible
Ansible behandelt router, switch en servers
Flask bewaart en toont output in SQLite
```

Dat is de essentie van de opdracht, maar in een vorm die binnen de tijd haalbaar en uitlegbaar blijft.
