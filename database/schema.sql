-- SQLite-schema voor dit project.
-- Verantwoordelijke: Joost
--
-- ============================================================
-- Tabel: users
-- ============================================================
-- Deze tabel bewaart de gebruikers die mogen aanmelden.

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

CREATE TABLE IF NOT EXISTS deployment_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,                               --   Uniek nummer voor elke logregel.
    user_id INTEGER NOT NULL,                                           --   Verwijst naar de gebruiker die de actie gestart heeft.
    setup_id INTEGER NOT NULL,                                          --   Verwijst naar de gekozen netwerkopstelling.
    timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,                  --   Het tijdstip waarop de logregel wordt aangemaakt.
    status TEXT NOT NULL CHECK (status IN ('success', 'failed')),       --   De status die terugkomt van Ansible.
    output TEXT NOT NULL,                                               --   De tekstuele output of foutmelding van Ansible.
    run_reference TEXT,                                                 --   Unieke naam voor 1 configuratierun.

    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (setup_id) REFERENCES network_setups(id)
);


-- ============================================================
-- Indexen
-- ============================================================
-- Een index helpt SQLite om sneller te zoeken.

CREATE INDEX IF NOT EXISTS idx_deployment_logs_user_id          --   handig als we later logs per gebruiker willen opvragen.
ON deployment_logs(user_id);

CREATE INDEX IF NOT EXISTS idx_deployment_logs_setup_id         --   handig als we later logs per netwerkopstelling willen opvragen.
ON deployment_logs(setup_id);

CREATE INDEX IF NOT EXISTS idx_deployment_logs_timestamp        --   handig om snel de laatste logregel te vinden.
ON deployment_logs(timestamp);
