# Changelog Joost

| Datum | Sprint | Bestand(en) | Wijziging | Waarom |
| --- | --- | --- | --- | --- |
| 2026-05-11 | Sprint 1 | `database/schema.sql` | SQLite-schema uitgewerkt met de tabellen `users`, `network_setups` en `deployment_logs`. | Deze tabellen zijn nodig voor login, het tonen van netwerkopstellingen en het bewaren van Ansible-output. |
| 2026-05-11 | Sprint 1 | `database/schema.sql` | Relaties toegevoegd tussen `deployment_logs`, `users` en `network_setups` via foreign keys. | Zo is elke logregel gekoppeld aan een bestaande gebruiker en een bestaande netwerkopstelling. |
| 2026-05-11 | Sprint 1 | `database/schema.sql` | Constraint toegevoegd op `status`, zodat alleen `success` of `failed` toegelaten wordt. | Dit volgt de koppelafspraak met de Ansible-helper. |
| 2026-05-11 | Sprint 1 | `database/schema.sql` | Indexen toegevoegd op `user_id`, `setup_id` en `timestamp` in `deployment_logs`. | Dit maakt latere zoekopdrachten en het ophalen van de laatste logregel logischer en sneller. |