# Changelog Lina

| Datum | Sprint | Bestand(en) | Wijziging | Waarom |
| --- | --- | --- | --- | --- |
| 11-05-2026 | Sprint 1 | `app.py` | Opzetten van de basis Flask-applicatie met routes voor login en dashboard | Initiële structuur voorzien voor de webinterface volgens de projectvereisten |
| 11-05-2026 | Sprint 1 | `login.html` | Ontwikkeling van loginformulier met invoervelden en foutmelding | Mogelijkheid creëren voor authenticatie van docenten |
| 11-05-2026 | Sprint 1 | `dashboard.html` | Aanmaken van dashboardpagina met weergave van gebruiker en netwerkopstellingen | Overzicht bieden van beschikbare configuraties na succesvolle login |
| 11-05-2026 | Sprint 1 | `dashboard.html` | Toevoegen van formulier met POST-methode voor starten van configuraties | Integratie mogelijk maken tussen frontend en Flask backend voor deploy acties |
| 11-05-2026 | Sprint 1 | `app.py` | Implementatie van deploy-route met subprocess voor Ansible en logging naar SQLite | Automatiseren van netwerkconfiguraties via playbooks en registreren van output |
| 11-05-2026 | Sprint 1 | `style.css` | Toevoegen van basis CSS en achtergrondafbeelding | Verbeteren van de gebruikerservaring en visuele aantrekkelijkheid |
| 11-05-2026 | Sprint 1 | `dashboard.html`, `login.html` | Integratie van Bootstrap via CDN | Zorgen voor een professionele en uniforme gebruikersinterface |
| ---- | ---- | ---- | ---- | ---- |
| 19-05-2026 | Sprint 2 | `docs/diagrams/netwerkdiagram.drawio` | Eerste versie van netwerkdiagram aangemaakt met 4 pods, routers en switches | Visuele voorstelling voorzien van de labo-opstelling |
| 19-05-2026 | Sprint 2 | `docs/diagrams/netwerkdiagram.drawio` | Toevoegen van centrale extension/bridge switch | Verbinding realiseren tussen pods en klaslokaal |
| 19-05-2026 | Sprint 2 | `docs/diagrams/netwerkdiagram.drawio` | Toevoegen van classroom switch en studentpoorten | Studenten moeten de pods vanuit het klaslokaal kunnen configureren |
| 19-05-2026 | Sprint 2 | `docs/diagrams/netwerkdiagram.drawio` | Uitwerken van de verbindingen tussen pods en extension switch | Correcte stertopologie voorzien volgens de opdracht |
| 19-05-2026 | Sprint 2 | `docs/diagrams/netwerkdiagram.drawio` | Aanpassen van de interne pod-topologie naar Router → Switch 1 → Switch 2 | Logische netwerkstructuur voorzien voor verdere configuratie |
| 21-05-2026 | Sprint 2 | `dashboard.html` | Herwerken van de dashboard-layout met verbeterde verdeling tussen configuratie- en monitoringgedeelte | Betere benutting van de beschikbare schermruimte |
| 21-05-2026 | Sprint 2 | `style.css` | Toevoegen van flex- en grid-layouts voor een responsieve dashboardweergave | Overzichtelijkere gebruikersinterface creëren |
| 21-05-2026 | Sprint 2 | `dashboard.html`, `style.css` | Scrollbare output-sectie toegevoegd voor "Laatste configuratie" | Lange Ansible-output leesbaar houden zonder de volledige pagina uit te rekken |
| 21-05-2026 | Sprint 2 | `dashboard.html` | Jinja-weergave aangepast voor arrays en lijsten binnen configuratievariabelen | Correcte weergave van Servers en andere lijstwaarden |
| 21-05-2026 | Sprint 2 | `style.css` | Login-gerelateerde CSS opnieuw geïntegreerd | Bestaande loginpagina behouden na dashboard-herwerking |
| 21-05-2026 | Sprint 2 | `style.css` | Header-overlay aangepast van rode tint naar neutrale transparantie | Achtergrondafbeelding beter zichtbaar maken |
| 21-05-2026 | Sprint 2 | `dashboard.html` | Nieuwe dashboard-iconen toegevoegd voor Gebruiker, Opstellingen en Laatste status | Visuele duidelijkheid verbeteren |
| 21-05-2026 | Sprint 2 | `style.css` | Statusweergave aangepast naar enkel gekleurde tekst zonder badge | Layout beter laten aansluiten bij het dashboardontwerp |
| 21-05-2026 | Sprint 2 | `dashboard.html`, `style.css` | Logout-knop uitgebreid met SVG exit-icoon | Duidelijkere navigatie voorzien voor gebruikers |
| 21-05-2026 | Sprint 2 | `style.css` | Media-query en logout-styling herwerkt | Problemen met schaal en weergave van de logout-knop oplossen |
| 26-05-2026 | Sprint 3 | `app.py`, `dashboard.html` | Configuratiegeschiedenis toegevoegd op basis van deployment logs uit de database. | Historiek van uitgevoerde configuraties zichtbaar maken voor de gebruiker. |
| 26-05-2026 | Sprint 3 | `modules/database_tools.py`, `dashboard.html` | Functionaliteit toegevoegd voor het ophalen en tonen van backupbestanden. | Backups inzichtelijk maken binnen het dashboard. |
| 26-05-2026 | Sprint 3 | `modules/database_tools.py` | Tijdstempels aangepast voor gebruik van Belgische tijd (Europe/Brussels). | Correcte tijdsregistratie van configuraties voorzien. |
| 26-05-2026 | Sprint 3 | `dashboard.html` | Dubbele technische output verwijderd uit configuratiegeschiedenis. | Dashboard overzichtelijker maken en dubbele informatie vermijden. |
| 26-05-2026 | Sprint 3 | `dashboard.html`, `style.css` | Configuratiegeschiedenis herwerkt naar uitklapbare dropdowns per configuratierun. | Grote hoeveelheden geschiedenis compacter weergeven. |
| 26-05-2026 | Sprint 3 | `dashboard.html`, `style.css` | Samenvatting van configuraties verborgen achter een klikbare setup-weergave. | Informatie enkel tonen wanneer nodig en de leesbaarheid verbeteren. |
| --- | --- | --- | --- | --- |




