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
| Setupdata | `setup1/info.yml` beschrijft de basisopstelling en bevat later ook configureerbare waarden. |
| Backups | Running-config van router en switch wordt als eenvoudige tekstbackup bewaard als dit technisch haalbaar is. |
| HTTP | Eigen Alpine-container met eenvoudige indexpagina. |
| HTTPS | Eigen Alpine-container met eenvoudige indexpagina en TLS/SSL. |
| FTP | Eigen Alpine-container met FTP-service en testbestand. |
| Docker Compose | Bestand om containers samen te bouwen/starten. |
| Testbaarheid | HTTP, HTTPS, FTP, router en switch moeten aantoonbaar getest of verantwoord worden. |
| Netwerkdocumentatie | IP-adresseringsschema en eenvoudig netwerkschema/podschema voorzien. |
| Documentatie | Uitleg over opstelling, keuzes, installatie en beperkingen. |

## Wat bouwen we beperkt?

| Onderdeel | Beperking | Waarom? |
| --- | --- | --- |
| Routerconfiguratie | Alleen minimum: hostname, interface/IP, routing, OSPF-basis. | Genoeg om de vereiste te tonen. |
| Switchconfiguratie | Alleen minimum: hostname, 2 VLANs, accesspoort, trunkpoort. | Genoeg om de vereiste te tonen. |
| Netwerkopstellingen | Eerst 1 basisopstelling onder `setup1`, met centrale setupdata. | Meerdere opstellingen maken het project groter. |
| Aanpasbare setupwaarden | Eerst technisch voorbereiden via `info.yml`, daarna beperkt via frontend. | Zo blijft de demo stabiel en vermijden we te veel validatielogica ineens. |
| Webinterface | Simpele pagina's, geen uitgebreide styling. | Functionaliteit is belangrijker dan uiterlijk. |
| Ansible-output | Output na uitvoering tonen, niet realtime. | Realtime output is complexer en optioneel. |
| Tweede netwerkopstelling | Alleen als de basisopstelling stabiel blijft. | Dit is nuttig voor de opgave, maar mag de demo niet onstabiel maken. |
| Backups | Alleen running-config ophalen en bewaren. | Geen volledig restore-systeem in de MVP. |

## Wat bouwen we niet in de MVP of enkel als de tijd het toelaat?

| Onderdeel | Waarom niet? |
| --- | --- |
| Adminpagina | Extra CRUD-functionaliteit is te groot voor de basis. |
| Meerdere uitgebreide netwerkopstellingen | Eerst 1 flow betrouwbaar maken. Een tweede eenvoudige voorbeeldopstelling kan alleen als er tijd over is. |
| Realtime output | Bonus, niet nodig voor de kern. |
| Volledig backup- en restoreplatform | We bewaren configuratiebackups, maar bouwen geen uitgebreid restorebeheer. |
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
Ansible kan configuratiebackups bewaren in backups/
```

Dat is de essentie van de opdracht, maar in een vorm die binnen de tijd haalbaar en uitlegbaar blijft.

## Uitbreiding na Sprint 1

Omdat Sprint 1 sneller ging dan verwacht, breiden we de MVP licht uit richting de opgave.

We proberen extra aan te tonen:

- router- en switchplaybooks zijn effectief getest in EVE-NG;
- HTTP-, HTTPS- en FTP-containers zijn bereikbaar of problemen zijn duidelijk verantwoord;
- output/status wordt opgeslagen en zichtbaar gemaakt;
- er komt een duidelijk IP-adresseringsschema;
- er komt een eenvoudig netwerkschema/podschema;
- `setup1/info.yml` wordt de centrale plaats voor setupinformatie en basisvariabelen;
- router- en switchconfiguraties kunnen als backup bewaard worden;
- eventueel komt er een tweede netwerkopstelling als de basis stabiel blijft.

We voegen geen grote nieuwe modules toe. Sprint 4 blijft voor testen, documentatie en oplevering.
