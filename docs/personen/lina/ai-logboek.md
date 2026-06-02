# AI-logboek Lina

| Datum | Sprint | Prompt / vraag | AI-tool | Resultaat | Zelf gecontroleerd |
| --- | --- | --- | --- | --- | --- |
| 11-05-2026 | Sprint 1 | Hoe bouw ik een Flask dashboard met login pagina door gebruik te maken van Python. | Copilot | Basisstructuur verkregen voor Flask-app met login en dashboard | Ja, getest door applicatie lokaal op te starten |
| 11-05-2026 | Sprint 1 | Ik vroeg voor verbeteringen in `dashboard.html`, `login.html` en `app.py`. | Copilot | Verkeerde Jinja syntax, missing form fields, fout in routes (/deploy, /dashboard), session problemen, CSS die niet geladen wordt| Ja, werkt correct |
| 11-05-2026 | Sprint 1 | Hoe integreer ik Bootstrap en CSS in Flask? | Copilot | CDN en static gebruik correct toegepast | Ja, styling zichtbaar |
| 11-05-2026 | Sprint 1 | Deploy knop werkt niet | Copilot |/deploy/{{ setup.id }} -> is fout, Deploy knop werkt → stuurt POST + setup_id | Ja, werkt correct |
| 11-05-2026 | Sprint 1 | Samenvatting van de hele project op dit moment | Copilot | `app.py` → correct, `dashboard.html` → gefixt, `login.html` → correct (nu verbeterd), CSS `style.css` → goed gekoppeld | Ja, nu ziet er beter uit|
| ---- | ---- | ---- | ---- | ---- | --- |
| 19-05-2026 | Sprint 2 | Ontwerp een netwerkdiagram waarbij 4 pods met routers en switches gebruikt kunnen worden vanuit een klaslokaal. Hoe moeten deze verbonden worden? | ChatGPT | Voorstel uitgewerkt met 4 pods, centrale extension/bridge switch en classroom switch. | Ja, zelf verwerkt in draw.io netwerkdiagram |
| 19-05-2026 | Sprint 2 | Wat betekent "20 poorten van een pod-switch dupliceren/beschikbaar maken in het klaslokaal"? | ChatGPT | Uitleg gekregen over trunkverbindingen, VLAN-doorgifte en het logisch beschikbaar maken van poorten voor studenten. | Ja, verwerkt in netwerkontwerp |
| 19-05-2026 | Sprint 2 | Hoe moeten de 4 pods verbonden worden met de extension/bridge switch? Wat is de beste voorstel/ techniek?  | ChatGPT | Stertopologie voorgesteld waarbij elke pod-switch verbonden wordt met de centrale extension switch. | Ja, toegepast in diagram |
| 19-05-2026 | Sprint 2 | Hoe moeten router en switches binnen een pod onderling verbonden worden? | ChatGPT | Router → Switch 1 → Switch 2 voorgesteld als standaardtopologie. | Ja, verwerkt in ontwerp |
| 19-05-2026 | Sprint 2 | Waar plaats ik het draw.io netwerkdiagram binnen de projectstructuur? | ChatGPT | Advies gekregen om netwerkdiagrammen onder docs/diagrams op te slaan voor documentatie. | Ja, projectstructuur aangepast |
| 21-05-2026 | Sprint 2 | Ik vroeg hulp bij het verbeteren van de dashboard-layout zodat de volledige schermruimte gebruikt wordt. | ChatGPT | Nieuwe dashboard-layout uitgewerkt met verbeterde verdeling tussen configuraties en monitoring. | Ja, getest in browser |
| 21-05-2026 | Sprint 2 | Hoe maak ik de sectie "Laatste configuratie" scrollbaar zonder de rest van de pagina te beïnvloeden? | ChatGPT | Scrollbare output-box voorzien met behoud van overzichtelijke layout. | Ja, getest met lange output |
| 21-05-2026 | Sprint 2 | Hoe kan ik de configuratievariabelen Router, Switch en Servers naast elkaar tonen? | ChatGPT | Nieuwe CSS-grid uitgewerkt zodat de variabelen overzichtelijk naast elkaar worden weergegeven. | Ja, gecontroleerd in dashboard |
| 21-05-2026 | Sprint 2 | Waarom worden de Servers niet weergegeven in de configuratievariabelen? | ChatGPT | Jinja-code aangepast zodat ook lijsten en arrays correct worden weergegeven. | Ja, Servers zijn zichtbaar |
| 21-05-2026 | Sprint 2 | Hoe kan ik de login-styling behouden na het herwerken van de dashboard CSS? | ChatGPT | Ontbrekende login-gerelateerde CSS terug toegevoegd. | Ja, loginpagina werkt opnieuw correct |
| 21-05-2026 | Sprint 2 | Hoe kan ik de rode overlay boven de headerafbeelding verwijderen? | ChatGPT | Overlay vervangen door neutrale donkere transparantie zodat de foto zichtbaar blijft. | Ja, visueel gecontroleerd |
| 21-05-2026 | Sprint 2 | Ik wil dezelfde dashboard-indeling en iconen zoals in de voorgestelde mock-up. | ChatGPT | Nieuwe iconen, statusweergave en layout uitgewerkt volgens het voorgestelde ontwerp. | Ja, gecontroleerd |
| 21-05-2026 | Sprint 2 | Hoe toon ik de status enkel als gekleurde tekst zonder badge? | ChatGPT | CSS aangepast zodat enkel de tekstkleur verandert voor Success en Failed. | Ja, werkt correct |
| 21-05-2026 | Sprint 2 | Ik wil een logout-knop met een exit-icoon. | ChatGPT | SVG exit-icoon toegevoegd aan de logout-knop. | Ja, getest |
| 21-05-2026 | Sprint 2 | Waarom wordt mijn logout-knop te groot door de media-query? | ChatGPT | CSS herwerkt zodat logout-styling buiten de media-query wordt toegepast. | Ja, probleem opgelost |
| 26-05-2026 | Sprint 3 | Analyseer mijn projectstructuur en controleer welke Sprint 3-taken nog ontbreken. | ChatGPT | Analyse uitgevoerd van Flask-, SQLite- en dashboardstructuur met overzicht van resterende Sprint 3-functionaliteiten. | Ja, vergeleken met projectvereisten |
| 26-05-2026 | Sprint 3 | Hoe kan ik configuratiegeschiedenis toevoegen aan het dashboard? | ChatGPT | Overzicht van deployment logs toegevoegd met weergave van eerdere configuraties. | Ja, getest in dashboard |
| 26-05-2026 | Sprint 3 | Hoe kan ik backupbestanden zichtbaar maken in het dashboard? | ChatGPT | Overzichtspaneel toegevoegd dat beschikbare backupbestanden weergeeft. | Ja, gecontroleerd |
| 26-05-2026 | Sprint 3 | Waarom komt het tijdstip niet overeen met de Belgische tijd? | ChatGPT | Aanpassing voorgesteld voor gebruik van Europe/Brussels tijdzone bij deployment logs. | Ja, getest met nieuwe configuratie |
| 26-05-2026 | Sprint 3 | Hoe verwijder ik de dubbele technische output uit configuratiegeschiedenis? | ChatGPT | Dubbele technische output verwijderd zodat deze enkel zichtbaar blijft bij Laatste Configuratie. | Ja, gecontroleerd |
| 26-05-2026 | Sprint 3 | Hoe maak ik van configuratiegeschiedenis een dropdown-overzicht? | ChatGPT | Uitklapbare configuratiegeschiedenis toegevoegd met gebruik van HTML details/summary. | Ja, getest |
| 26-05-2026 | Sprint 3 | Hoe toon ik samenvattingen enkel wanneer op een setup geklikt wordt? | ChatGPT | Samenvattingen verborgen achter een dropdown per configuratierun. | Ja, gecontroleerd |
| --- | --- | --- | --- | --- | --- |






