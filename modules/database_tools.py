# Hier komen de SQLite-hulpfuncties.
#
# Verantwoordelijke: Joost
#
# Dit bestand vormt de backend-laag tussen Flask en SQLite.
#
# Simpel gezegd:
# - app.py mag niet rechtstreeks ingewikkelde SQL-code moeten schrijven;
# - app.py roept functies uit dit bestand op;
# - dit bestand praat met de SQLite-database.
#
# Voorbeeld:
# Lina maakt in app.py een loginformulier.
# Dat formulier stuurt username en password door.
# app.py roept dan verify_user(username, password) op.
# Deze functie controleert de gebruiker in SQLite.


import sqlite3
from pathlib import Path
from werkzeug.security import generate_password_hash, check_password_hash


# ============================================================
# Padinstellingen
# ============================================================
# __file__ verwijst naar dit bestand:
# modules/database_tools.py
#
# Path(__file__).resolve()
# geeft het volledige pad naar dit bestand.
#
# .parent
# gaat naar de map modules.
#
# .parent.parent
# gaat naar de hoofdmap van het project.
#
# Daardoor werkt deze code ook als je het project op een andere pc zet.
BASE_DIR = Path(__file__).resolve().parent.parent

# Dit is het pad naar de echte SQLite-database.
# De database komt in de map data.
DATABASE_PATH = BASE_DIR / "data" / "itproject.db"

# Dit is het pad naar het SQL-schema dat we in Sprint 1 gemaakt hebben.
SCHEMA_PATH = BASE_DIR / "database" / "schema.sql"


def get_connection():
    """
    Maakt een verbinding met de SQLite-database.

    Waarom een aparte functie?
    - Dan moeten we niet overal sqlite3.connect(...) opnieuw schrijven.
    - We zetten hier ook meteen foreign keys aan.
    - We zorgen dat rijen makkelijker als dictionaries gebruikt kunnen worden.

    Return:
    - een actieve databaseverbinding.
    """

    # Zorgt ervoor dat de map data bestaat.
    # Als de map al bestaat, gebeurt er niets.
    DATABASE_PATH.parent.mkdir(exist_ok=True)

    # Maakt verbinding met de database.
    # Als itproject.db nog niet bestaat, maakt SQLite dit bestand automatisch aan.
    connection = sqlite3.connect(DATABASE_PATH)

    # Zorgt ervoor dat we kolommen op naam kunnen aanspreken.
    # Bijvoorbeeld row["username"] in plaats van row[1].
    connection.row_factory = sqlite3.Row

    # SQLite controleert foreign keys niet altijd automatisch.
    # Hiermee activeren we die controle per verbinding.
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def init_database():
    """
    Maakt de SQLite-database klaar.

    Verantwoordelijke: Joost

    Verwacht gedrag:
    - leest database/schema.sql in;
    - maakt de tabellen aan als ze nog niet bestaan;
    - zorgt voor een eerste testdocent.

    Wordt gebruikt door:
    - Lina in app.py bij het opstarten van de Flask-applicatie.

    Return:
    - niets.
    """

    # We openen een verbinding met de database.
    connection = get_connection()

    # We lezen het schema.sql-bestand in.
    # Daarin staan de CREATE TABLE-opdrachten uit Sprint 1.
    with open(SCHEMA_PATH, "r", encoding="utf-8") as schema_file:
        schema_sql = schema_file.read()

    # executescript kan meerdere SQL-opdrachten na elkaar uitvoeren.
    # Dat is nodig omdat schema.sql meerdere CREATE TABLE-statements bevat.
    connection.executescript(schema_sql)

    # We maken een eerste testdocent aan.
    # Dit is handig zodat Lina later de login kan testen.
    #
    # Belangrijk:
    # We slaan NIET het gewone wachtwoord op.
    # We slaan een hash op van "docent123".
    #
    # Testlogin:
    # gebruikersnaam: docent
    # wachtwoord: docent123
    password_hash = generate_password_hash("docent123")

    # INSERT OR IGNORE betekent:
    # - voeg de gebruiker toe als hij nog niet bestaat;
    # - doe niets als username "docent" al bestaat.
    #
    # Dat is handig omdat username UNIQUE is in schema.sql.
    connection.execute(
        """
        INSERT OR IGNORE INTO users (username, password_hash, role)
        VALUES (?, ?, ?)
        """,
        ("docent", password_hash, "teacher"),
    )

    # We bewaren de wijzigingen.
    connection.commit()

    # We sluiten de verbinding netjes af.
    connection.close()


def verify_user(username, password):
    """
    Controleert of een docent mag aanmelden.

    Verantwoordelijke: Joost

    Parameters:
    - username: gebruikersnaam uit het loginformulier.
    - password: wachtwoord uit het loginformulier.

    Verwacht gedrag:
    - zoekt de gebruiker op in de tabel users;
    - controleert het wachtwoord met password hashing;
    - geeft alleen een gebruiker terug als de login klopt.

    Return bij succes:
    {
        "id": 1,
        "username": "docent",
        "role": "teacher"
    }

    Return bij fout:
    - None
    """

    # Kleine veiligheid:
    # Als username of password leeg is, stoppen we meteen.
    if not username or not password:
        return None

    connection = get_connection()

    # We zoeken de gebruiker op basis van username.
    #
    # De ? is een parameter.
    # Dat is veiliger dan zelf strings samen te plakken.
    # Zo vermijden we SQL injection.
    user = connection.execute(
        """
        SELECT id, username, password_hash, role
        FROM users
        WHERE username = ?
        """,
        (username,),
    ).fetchone()

    connection.close()

    # Als er geen gebruiker gevonden is, is de login fout.
    if user is None:
        return None

    # check_password_hash vergelijkt:
    # - het wachtwoord dat de gebruiker intypt;
    # - met de hash die in de database staat.
    #
    # Als het niet klopt, geven we None terug.
    if not check_password_hash(user["password_hash"], password):
        return None

    # Als alles klopt, geven we alleen veilige info terug.
    # We geven dus bewust password_hash niet terug.
    return {
        "id": user["id"],
        "username": user["username"],
        "role": user["role"],
    }


def get_network_setups():
    """
    Geeft de beschikbare netwerkopstellingen terug.

    Verantwoordelijke: Joost

    Verwacht gedrag:
    - leest alle opstellingen uit de tabel network_setups;
    - geeft simpele data terug die Lina direct in het dashboard kan tonen.

    Belangrijk:
    - Joost voorziet de databasefunctie.
    - Bart bepaalt inhoudelijk welke netwerkopstellingen/playbooks erin komen.

    Return:
    [
        {
            "id": 1,
            "name": "Basisopstelling",
            "description": "1 router, 1 switch, HTTP, HTTPS en FTP"
        }
    ]
    """

    connection = get_connection()

    # We halen alle netwerkopstellingen op.
    # We tonen hier bewust niet playbook_data,
    # omdat Lina op het dashboard meestal alleen id, name en description nodig heeft.
    rows = connection.execute(
        """
        SELECT id, name, description
        FROM network_setups
        ORDER BY id
        """
    ).fetchall()

    connection.close()

    # We zetten elke SQLite-rij om naar een gewone dictionary.
    # Dat is makkelijker voor Flask en templates.
    network_setups = []

    for row in rows:
        network_setups.append(
            {
                "id": row["id"],
                "name": row["name"],
                "description": row["description"],
            }
        )

    return network_setups


def save_deployment_log(user_id, setup_id, status, output):
    """
    Slaat het resultaat van een Ansible-uitvoering op.

    Verantwoordelijke: Joost

    Parameters:
    - user_id: id van de aangemelde docent.
    - setup_id: id van de gekozen netwerkopstelling.
    - status: "success" of "failed".
    - output: tekstuele output of foutmelding van Ansible.

    Verwacht gedrag:
    - schrijft een nieuwe regel in deployment_logs;
    - bewaart timestamp, status en output.

    Return:
    - niets.
    """

    # Extra controle in Python.
    # In schema.sql staat ook al een CHECK constraint,
    # maar zo geven we sneller een duidelijke fout als de status fout is.
    if status not in ("success", "failed"):
        raise ValueError("status moet 'success' of 'failed' zijn")

    connection = get_connection()

    # We voegen een nieuwe logregel toe.
    #
    # timestamp geven we niet mee.
    # SQLite vult dat automatisch in via DEFAULT CURRENT_TIMESTAMP.
    connection.execute(
        """
        INSERT INTO deployment_logs (user_id, setup_id, status, output)
        VALUES (?, ?, ?, ?)
        """,
        (user_id, setup_id, status, output),
    )

    connection.commit()
    connection.close()


def get_last_deployment_log():
    """
    Geeft de laatste Ansible-uitvoering terug.

    Verantwoordelijke: Joost

    Verwacht gedrag:
    - leest de nieuwste regel uit deployment_logs;
    - geeft die terug zodat Lina ze op het dashboard kan tonen.

    Return als er een log bestaat:
    {
        "id": 1,
        "user_id": 1,
        "setup_id": 1,
        "timestamp": "2026-05-07 10:00:00",
        "status": "success",
        "output": "Ansible-output..."
    }

    Return als er nog geen log is:
    - None
    """

    connection = get_connection()

    # We vragen de nieuwste logregel op.
    # ORDER BY id DESC betekent:
    # hoogste id eerst, dus de laatste toegevoegde log.
    #
    # LIMIT 1 betekent:
    # geef maar 1 resultaat terug.
    row = connection.execute(
        """
        SELECT id, user_id, setup_id, timestamp, status, output
        FROM deployment_logs
        ORDER BY id DESC
        LIMIT 1
        """
    ).fetchone()

    connection.close()

    # Als er nog geen deployment logs zijn, geven we None terug.
    if row is None:
        return None

    # We zetten de SQLite-rij om naar een gewone dictionary.
    return {
        "id": row["id"],
        "user_id": row["user_id"],
        "setup_id": row["setup_id"],
        "timestamp": row["timestamp"],
        "status": row["status"],
        "output": row["output"],
    }