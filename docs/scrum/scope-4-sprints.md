# Scope over 4 sprints

## Doel

We werken het project af in 4 sprints. Elke sprint eindigt met een werkende versie die niet afhankelijk is van latere sprints.

De MVP blijft:

```text
Docent logt in -> kiest 1 netwerkopstelling -> Flask start Ansible -> output/status komt in SQLite.
```

Ansible richt zich op:

- 1 router;
- 1 switch;
- HTTP-container;
- HTTPS-container;
- FTP-container.

## Sprintoverzicht

| Sprint | Doel | Resultaat op het einde |
| --- | --- | --- |
| Sprint 1 | Basis en taakverdeling | Structuur, documenten, placeholders, SQLite-schema, Flask-pagina's en Docker/Ansible-basis staan klaar. |
| Sprint 2 | Flask en SQLite werkend maken | Docentlogin, dashboard, 1 netwerkopstelling en deployment logs werken lokaal. |
| Sprint 3 | Ansible en Docker koppelen | Flask kan Ansible starten en Dockercontainers voor HTTP/HTTPS/FTP zijn testbaar. |
| Sprint 4 | Integratie, test en einddocumentatie | Volledige demo-flow testen, beperkingen verantwoorden en documentatie finaliseren. |

## Taakverdeling per sprint

### Sprint 1 - Basis

| Persoon | Focus |
| --- | --- |
| Lina | Login- en dashboardtemplates klaarzetten. |
| Joost | SQLite-schema uitwerken. |
| Bart | Inventory, playbook-placeholders en Dockerbasis controleren. |

### Sprint 2 - Flask + SQLite

| Persoon | Focus |
| --- | --- |
| Lina | Login/dashboard koppelen aan backendfuncties. |
| Joost | Database initialiseren, users/network_setups/logs voorzien. |
| Bart | Ansible-helper voorbereiden met vaste outputstructuur. |

### Sprint 3 - Ansible + Docker

| Persoon | Focus |
| --- | --- |
| Lina | Startknop en resultaatweergave afwerken. |
| Joost | Deployment logs opslaan en uitlezen. |
| Bart | Router/switch/serverplaybooks en Dockercontainers testen. |

### Sprint 4 - Integratie + documentatie

| Persoon | Focus |
| --- | --- |
| Lina | Demo-flow door de webinterface tonen. |
| Joost | Database/logs controleren en documenteren. |
| Bart | Docker/Ansible/demo testen en beperkingen documenteren. |

## Afspraken

- `main` blijft werkend.
- Elke sprint heeft een review en retrospective.
- Could have-taken worden alleen gedaan als de Must have-taken werken.
- Als iets niet lukt, documenteren we eerlijk waarom.

