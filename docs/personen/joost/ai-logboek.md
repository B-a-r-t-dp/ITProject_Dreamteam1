# AI-logboek Joost

| Datum | Sprint | Prompt / vraag | AI-tool | Resultaat | Zelf gecontroleerd |
| 2026-05-11| Sprint 1 | Ik heb gevraagd om de projectstructuur, sprintdocumentatie en mijn rol als database-eigenaar te analyseren. | ChatGPT | Duidelijker beeld gekregen dat mijn Sprint 1-taak vooral `database/schema.sql` is. | Ja, gecontroleerd met `docs/scrum/sprint-1.md` en `docs/koppelafspraken.md`. |
| 2026-05-11| Sprint 1 | Ik heb gevraagd welke SQLite-tabellen nodig zijn voor de MVP. | ChatGPT | Bevestigd dat `users`, `network_setups` en `deployment_logs` verplicht zijn. | Ja, gecontroleerd met `docs/mvp-afbakening.md`. |
| 2026-05-11| Sprint 1 | Ik heb gevraagd hoe ik de relaties tussen gebruikers, netwerkopstellingen en deployment logs best opbouw. | ChatGPT | Foreign keys voorzien van `deployment_logs.user_id` naar `users.id` en van `deployment_logs.setup_id` naar `network_setups.id`. | Ja, gecontroleerd of dit overeenkomt met de vaste veldnamen. |
| 2026-05-11| Sprint 1 | Ik heb gevraagd waarom wachtwoorden niet als gewone tekst opgeslagen mogen worden. | ChatGPT | Uitleg gekregen dat de tabel een `password_hash` moet bevatten, zodat Sprint 2 met password hashing kan werken. | Ja, dit komt overeen met de MVP-afbakening. |
| 2026-05-11| Sprint 1 | Ik heb gevraagd waarom de status in `deployment_logs` best beperkt wordt tot `success` en `failed`. | ChatGPT | Een `CHECK`-constraint toegevoegd zodat de database dezelfde afspraken volgt als `modules/ansible_tools.py`. | Ja, gecontroleerd met `docs/koppelafspraken.md`. |

