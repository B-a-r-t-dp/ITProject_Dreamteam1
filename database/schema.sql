-- SQLite-schema voor dit project.
-- Verantwoordelijke: Joost
--
-- Doel van dit bestand:
-- - de verplichte SQLite-tabellen aanmaken;
-- - gebruikers bewaren voor de login;
-- - netwerkopstellingen bewaren voor het dashboard;
-- - deployment logs bewaren met status/output van Ansible;
-- - relaties leggen tussen gebruikers, netwerkopstellingen en logs.
--
-- Dit bestand wordt later in Sprint 2 gebruikt door:
-- modules/database_tools.py
--
-- Belangrijk:
-- We gebruiken hier vaste tabelnamen en veldnamen uit docs/koppelafspraken.md.
-- Die namen mogen niet zomaar gewijzigd worden, want app.py en database_tools.py
-- zullen later op deze structuur rekenen.


-- ============================================================
-- Tabel: users
-- ============================================================
-- Deze tabel bewaart de gebruikers die mogen aanmelden.
-- In onze MVP is dat minstens 1 docent.
--
-- id:
--   Uniek nummer voor elke gebruiker.
--
-- username:
--   De loginnaam van de gebruiker.
--   UNIQUE betekent dat dezelfde gebruikersnaam maar 1 keer mag bestaan.
--
-- password_hash:
--   Hier komt niet het echte wachtwoord in gewone tekst.
--   Hier komt later een gehashte versie van het wachtwoord.
--   Dat is veiliger en staat ook zo in de MVP-afbakening.
--
-- role:
--   De rol van de gebruiker.
--   Voor de MVP gebruiken we bijvoorbeeld 'teacher'.
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'teacher'
);


-- ============================================================
-- Tabel: network_setups
-- ============================================================
-- Deze tabel bewaart de netwerkopstellingen die de docent kan kiezen.
-- In de MVP starten we met minstens 1 basisopstelling.
--
-- id:
--   Uniek nummer voor elke netwerkopstelling.
--
-- name:
--   De naam die de docent op het dashboard ziet.
--
-- description:
--   Korte uitleg over wat de opstelling bevat.
--
-- playbook_data:
--   Extra info voor de Ansible-flow.
--   Bart kan dit later gebruiken om te bepalen welke playbooks horen
--   bij deze opstelling.
--   We bewaren dit als TEXT, zodat er later bijvoorbeeld JSON-tekst in kan staan.
CREATE TABLE IF NOT EXISTS network_setups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    playbook_data TEXT NOT NULL
);


-- ============================================================
-- Tabel: deployment_logs
-- ============================================================
-- Deze tabel bewaart het resultaat van elke configuratie-uitvoering.
-- Telkens wanneer Flask later Ansible start, komt hier een nieuwe logregel.
--
-- id:
--   Uniek nummer voor elke logregel.
--
-- user_id:
--   Verwijst naar de gebruiker die de actie gestart heeft.
--   Dit veld verwijst naar users(id).
--
-- setup_id:
--   Verwijst naar de gekozen netwerkopstelling.
--   Dit veld verwijst naar network_setups(id).
--
-- timestamp:
--   Het tijdstip waarop de logregel wordt aangemaakt.
--   DEFAULT CURRENT_TIMESTAMP zorgt ervoor dat SQLite automatisch
--   de huidige datum en tijd invult.
--
-- status:
--   De status die terugkomt van Ansible.
--   Volgens de koppelafspraken gebruiken we 'success' of 'failed'.
--   De CHECK voorkomt dat er per ongeluk iets anders wordt opgeslagen.
--
-- output:
--   De tekstuele output of foutmelding van Ansible.
CREATE TABLE IF NOT EXISTS deployment_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    setup_id INTEGER NOT NULL,
    timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL CHECK (status IN ('success', 'failed')),
    output TEXT NOT NULL,

    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (setup_id) REFERENCES network_setups(id)
);


-- ============================================================
-- Indexen
-- ============================================================
-- Een index helpt SQLite om sneller te zoeken.
-- Deze indexen zijn niet strikt verplicht, maar ze zijn logisch:
--
-- idx_deployment_logs_user_id:
--   handig als we later logs per gebruiker willen opvragen.
--
-- idx_deployment_logs_setup_id:
--   handig als we later logs per netwerkopstelling willen opvragen.
--
-- idx_deployment_logs_timestamp:
--   handig om snel de laatste logregel te vinden.
CREATE INDEX IF NOT EXISTS idx_deployment_logs_user_id
ON deployment_logs(user_id);

CREATE INDEX IF NOT EXISTS idx_deployment_logs_setup_id
ON deployment_logs(setup_id);

CREATE INDEX IF NOT EXISTS idx_deployment_logs_timestamp
ON deployment_logs(timestamp);