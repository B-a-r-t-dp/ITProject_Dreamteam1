# Retrospective Sprint 4

## Wat ging goed?

- De MVP werd klaargemaakt als eindversie. De focus lag niet meer op grote nieuwe functies, maar op testen, documenteren en voorbereiden van de demo.
- De technische documentatie werd afgewerkt volgens de onderdelen uit de opgave. Setup1, setup2, Docker, Flask, SQLite en Ansible worden daarin als 1 geheel uitgelegd.
- De code werd per eigenaar nagelezen en beter gedocumenteerd. Daardoor kunnen Bart, Lina en Joost alle bestanden begrijpen.
- Setup1 en setup2 zijn duidelijker gedocumenteerd. Per setup is nu beter zichtbaar welke toestellen, management-IP's, interfaces en configuraties erbij horen.
- De demo-flow is duidelijker geworden: aanmelden, setup kiezen, waarden aanpassen, configuratie starten, output bekijken, geschiedenis controleren en backups downloaden.
- De configuratiegeschiedenis en backupkoppeling maken het makkelijker om te bewijzen wat de applicatie effectief heeft gedaan.
- De Scrum-documenten, changelogs en AI-logboeken werden nagekeken zodat het projectverloop beter verdedigbaar is.
- De samenwerking bleef duidelijk verdeeld: Bart focuste op Ansible/Docker/netwerk, Joost op SQLite/backend en Lina op Flask/frontend/documentatie.

## Wat ging moeilijk?

- De technische documentatie vroeg meer tijd dan verwacht. Omdat de applicatie tijdens Sprint 3 nog gegroeid was, moesten meerdere stukken opnieuw afgestemd worden op de echte projectstatus, rekeninghoudend met de geemuleerde hardware wat beperkingen met zich mee gaf.
- De demo testen op een realistische omgeving was niet altijd eenvoudig. EVE-NG, VPN, hotspot, Debian VM en Docker moesten allemaal tegelijk goed meewerken.
- De VirtualBox/Debian-testomgeving gaf soms extra problemen, zoals pauzeren, schijfproblemen of netwerkbereikbaarheid. Dat was niet direct een fout in de applicatie, maar het maakte testen wel moeilijker.
- De Ansible-waarschuwingen blijven zichtbaar in de technische output. We hebben beslist om die te kunnen verantwoorden in plaats van ze kunstmatig te verbergen.
- Het was soms zoeken naar de juiste balans tussen veel commentaar en leesbare code. Te weinig uitleg is moeilijk voor de evaluatie, maar te veel commentaar maakt bestanden ook zwaarder.

## Wat nemen we mee naar de evaluatie?

- We tonen eerst de applicatie als volledige flow, niet als losse bestanden.
- We leggen duidelijk uit dat `info.yml` de centrale bron is voor setupwaarden.
- We tonen dat Flask niet zelf netwerkcommando's uitvoert, maar via `ansible_tools.py` Ansible start.
- We gebruiken de configuratiegeschiedenis en running-config backups als bewijs dat configuraties echt uitgevoerd werden.
- We vermelden eerlijk dat dit een MVP is:
  - wel configureren en controleren;
  - wel logs en backups tonen;
  - geen volledig productieplatform;
  - geen realtime Ansible-streaming;
  - geen uitgebreid restore-systeem.
- We bereiden ons erop voor om de SSH/EVE-NG-waarschuwingen en self-signed certificaten in mensentaal uit te leggen.

## Actiepunten voor de evaluatie

| Actie | Eigenaar | Status |
| --- | --- | --- |
| Technisch document finaal nalezen en klaarzetten om af te geven. | Team | Done |
| Demo-flow nog 1 keer volledig doorlopen. | Team | Done |
| Running-config bewijs klaarzetten voor setup1 en setup2. | Bart | Done |
| Code-uitleg per eigenaar voorbereiden. | Bart, Lina en Joost | Done |
| Changelogs en AI-logboeken controleren. | Team | Done |
| Scrum-documenten gelijkzetten met de eindstatus. | Team | Done |
