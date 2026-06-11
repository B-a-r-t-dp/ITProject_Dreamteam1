
# =====================================================================
#
# WAT DOET DIT BESTAND?
# ---------------------------------------------------------------------
# Dit bestand bevat alle hulpfuncties om met de SQLite-database te werken.
# Je kan dit bestand zien als de database-laag van de applicatie.
#
# In plaats van SQL-query's rechtstreeks in app.py te schrijven, roept app.py
# functies uit dit bestand aan.


import sqlite3                                                              # sqlite3 is de standaard Python-module om met SQLite-databases te werken.
from pathlib import Path                                                    # pathlib.Path gebruiken we om bestandspaden op een nette manier op te bouwen.
import yaml                                                                 # yaml gebruiken we om info.yml-bestanden te lezen.
from werkzeug.security import generate_password_hash, check_password_hash   # Werkzeug levert functies om wachtwoorden veilig te hashen en te controleren.
from datetime import datetime                                               # datetime gebruiken we voor tijdstippen van deployment logs en backups.
from zoneinfo import ZoneInfo                                               # ZoneInfo gebruiken we zodat tijdstippen in Belgische tijd kunnen worden gezet.


# =====================================================================
# CENTRALE PADEN
# =====================================================================
# BASE_DIR wordt dus de hoofdmap van het project.
# =====================================================================

BASE_DIR = Path(__file__).resolve().parent.parent                           #Bouwt het absolute pad naar de projectroot op,vertrekkend vanuit database_tools.py


# De database wordt bewust in de map data/ geplaatst.
DATABASE_PATH = BASE_DIR / "data" / "itproject.db"

# Pad naar het SQL-schema dat de tabellen aanmaakt.
SCHEMA_PATH = BASE_DIR / "database" / "schema.sql"

# Pad naar de Ansible-playbooks.
# Elke setup, zoals setup1 of setup2, heeft daar een eigen map.
PLAYBOOK_DIR = BASE_DIR / "ansible" / "playbooks"


# =====================================================================
# FUNCTIE: get_connection()
# =====================================================================
def get_connection():
    """
    Maakt verbinding met de SQLite-database.
    """

    # DATABASE_PATH.parent is de map data/.
    DATABASE_PATH.parent.mkdir(exist_ok=True)

    # sqlite3.connect() opent de database.
    connection = sqlite3.connect(DATABASE_PATH)

    # row_factory = sqlite3.Row zorgt ervoor zorgt ervoor dat we de resultaten uit de database kunnen opvragen via de kolomnamen.
    connection.row_factory = sqlite3.Row

    # SQLite controleert foreign keys niet altijd automatisch.
    connection.execute("PRAGMA foreign_keys = ON")

    # De verbinding wordt teruggegeven aan de functie die ze nodig heeft.
    return connection


# =====================================================================
# FUNCTIE: init_database()
# =====================================================================
def init_database():
    """
    Initialiseert de database.
    """
    # Open een verbinding met de database.
    connection = get_connection()

    # Lees het volledige schema.sql-bestand in.
    # encoding="utf-8" zorgt dat speciale tekens correct gelezen worden.
    with open(SCHEMA_PATH, "r", encoding="utf-8") as schema_file:
        schema_sql = schema_file.read()

    # executescript() kan meerdere SQL-statements na elkaar uitvoeren.
    # Dat is nodig omdat schema.sql meerdere CREATE TABLE- en CREATE INDEX-
    # statements bevat.
    connection.executescript(schema_sql)

    # Deze try/except is bedoeld voor bestaande databases.
    try:
        connection.execute("ALTER TABLE deployment_logs ADD COLUMN run_reference TEXT")
    except sqlite3.OperationalError:
        pass

    # We maken een hash van het testwachtwoord.
    password_hash = generate_password_hash("docent123")

    # Voeg standaardgebruikers toe.
    connection.executemany(
        """
        INSERT OR IGNORE INTO users (username, password_hash, role)
        VALUES (?, ?, ?)
        """,
        [
            ("docent", password_hash, "teacher 1"),
            ("docent2", password_hash, "teacher 2"),
        ],
    )

    # Lijst met standaard netwerkopstellingen voor de MVP.
    network_setups = [
        (
            1,
            "Basisopstelling",
            "1 router, 1 switch, HTTP, HTTPS en FTP",
            "setup1",
        ),
        (
            2,
            "Podopstelling Brussel",
            "1 pod met router, 2 pod-switches, distributieswitch en classroomswitch",
            "setup2",
        ),
    ]

    # Voeg de netwerkopstellingen toe als ze nog niet bestaan.
    connection.executemany(
        """
        INSERT OR IGNORE INTO network_setups
        (id, name, description, playbook_data)
        VALUES (?, ?, ?, ?)
        """,
        network_setups,
    )

    # Werk bestaande netwerkopstellingen bij.
    connection.executemany(
        """
        UPDATE network_setups
        SET name = ?, description = ?, playbook_data = ?
        WHERE id = ?
        """,
        [
            # Hier herschikken we de volgorde van het tuple.
            (setup[1], setup[2], setup[3], setup[0])
            for setup in network_setups
        ],
    )

    # commit() schrijft alle wijzigingen definitief weg naar de database.
    connection.commit()

    # Sluit de verbinding netjes af.
    connection.close()


# =====================================================================
# FUNCTIE: verify_user(username, password)
# =====================================================================
def verify_user(username, password):
    """
    Controleert of een gebruiker mag aanmelden.

    Deze functie wordt gebruikt bij de login.

    Input:
    - username: de ingegeven gebruikersnaam;
    - password: het ingegeven wachtwoord.

    Werking:
    1. Controleer of username en password ingevuld zijn.
    2. Zoek de gebruiker op in de tabel users.
    3. Als de gebruiker niet bestaat: return None.
    4. Controleer het wachtwoord met check_password_hash().
    5. Als het wachtwoord fout is: return None.
    6. Als alles klopt: geef een dictionary terug met usergegevens.

    Return bij correcte login:
    {
        "id": 1,
        "username": "docent",
        "role": "teacher 1"
    }

    Return bij fout:
    None
    """

    # Als username of password leeg is, stoppen we meteen.
    # Dan heeft het geen zin om de database te raadplegen.
    if not username or not password:
        return None

    # Open databaseverbinding.
    connection = get_connection()

    # Zoek de gebruiker op basis van username.
    user = connection.execute(
        """
        SELECT id, username, password_hash, role
        FROM users
        WHERE username = ?
        """,
        (username,),
    ).fetchone()

    # De query is uitgevoerd, dus de verbinding mag dicht.
    connection.close()

    # fetchone() geeft None terug als er geen gebruiker gevonden werd.
    if user is None:
        return None

    # Controleer het ingegeven wachtwoord tegenover de hash uit de database.
    if not check_password_hash(user["password_hash"], password):
        return None

    # Als alles correct is, geven we alleen de nodige userinformatie terug.
    return {
        "id": user["id"],
        "username": user["username"],
        "role": user["role"],
    }


# =====================================================================
# FUNCTIE: get_network_setups()
# =====================================================================
def get_network_setups():
    """
    Haalt alle beschikbare netwerkopstellingen op.

    app.py gebruikt deze functie om het dashboard te vullen.

    Wat doet deze functie?
    1. Lees alle records uit de tabel network_setups.
    2. Sorteer ze op id zodat ze in vaste volgorde verschijnen.
    3. Lees per setup extra informatie uit info.yml.
    4. Zet alles om naar een lijst van dictionaries.

    Waarom dictionaries?
    Templates zoals dashboard.html kunnen makkelijker werken met duidelijke
    sleutels zoals setup.name, setup.description en setup.info.
    """

    connection = get_connection()

    # Haal alle netwerkopstellingen uit de database.
    rows = connection.execute(
        """
        SELECT id, name, description, playbook_data
        FROM network_setups
        ORDER BY id
        """
     ).fetchall()

    connection.close()

    # We bouwen een gewone Python-lijst op voor gebruik in app.py/templates.
    network_setups = []

    for row in rows:
        # playbook_data bevat bijvoorbeeld "setup1" of "setup2".
        setup_info = get_setup_info(row["playbook_data"])

        # Voeg één setup toe als dictionary.
        network_setups.append(
            {
                "id": row["id"],
                "name": row["name"],
                "description": row["description"],
                "playbook_data": row["playbook_data"],
                "info": setup_info,
            }
        )

    return network_setups


# =====================================================================
# FUNCTIE: get_setup_info(setup_folder)
# =====================================================================
def get_setup_info(setup_folder):
    """
    Leest extra informatie over een netwerkopstelling.

    setup_folder is meestal "setup1" of "setup2".

    De functie zoekt naar:

        ansible/playbooks/<setup_folder>/info.yml

    """

    # Bouw het pad naar info.yml op.
    info_path = PLAYBOOK_DIR / setup_folder / "info.yml"

    # Als het info.yml-bestand niet bestaat, geven we None terug.
    if not info_path.exists():
        return None

    # Lees het YAML-bestand en zet het om naar Python-data.
    with open(info_path, "r", encoding="utf-8") as info_file:
        return yaml.safe_load(info_file)

# =====================================================================
# FUNCTIE: save_deployment_log(...)
# =====================================================================
def save_deployment_log(user_id, setup_id, status, output, run_reference=None):
    """
    Slaat het resultaat van een Ansible-uitvoering op.

    Deze functie wordt aangeroepen nadat een configuratie via Ansible
    uitgevoerd werd.

    Input:
    - user_id:
      De gebruiker die de configuratie gestart heeft.

    - setup_id:
      De netwerkopstelling die gekozen werd.

    - status:
      Het resultaat van de configuratie.
      Toegelaten waarden zijn "success" en "failed".

    - output:
      De tekstuele output van Ansible of van onze eigen samenvatting.

    - run_reference:
      Een unieke referentie voor deze configuratierun.
      Die wordt gebruikt om de juiste backupmap te koppelen aan deze log.

    """

    # Controleer dat status alleen success of failed mag zijn.
    if status not in ("success", "failed"):
        raise ValueError("status moet 'success' of 'failed' zijn")

    # Maak een timestamp in Belgische tijd.
    belgian_time = datetime.now(ZoneInfo("Europe/Brussels")).strftime("%Y-%m-%d %H:%M:%S")

    connection = get_connection()

    # Voeg één nieuwe logregel toe.
    connection.execute(
        """
        INSERT INTO deployment_logs (user_id, setup_id, timestamp, status, output, run_reference)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (user_id, setup_id, belgian_time, status, output, run_reference),
    )

    # Schrijf de INSERT definitief weg.
    connection.commit()

    # Sluit de verbinding.
    connection.close()


# =====================================================================
# FUNCTIE: split_deployment_output(output)
# =====================================================================
def split_deployment_output(output):
    """
    Splitst de Ansible-output in twee delen:
    """

    marker = "TECHNISCHE OUTPUT"

    # Als output leeg is of de marker ontbreekt, kunnen we niet splitsen.
    if not output or marker not in output:
        return {
            "summary": output,
            "technical_output": "",
        }

    # split(marker, 1) splitst maar één keer.
    summary, technical_output = output.split(marker, 1)

    # Verwijder de titel uit de samenvatting zodat het dashboard properder toont.
    summary = summary.replace("SAMENVATTING CONFIGURATIE", "").strip()

    # strip() verwijdert overbodige spaties en lege regels aan begin/einde.
    technical_output = technical_output.strip()

    return {
        "summary": summary,
        "technical_output": technical_output,
    }


# =====================================================================
# FUNCTIE: get_last_deployment_log(user_id=None)
# =====================================================================
def get_last_deployment_log(user_id=None):
    """
    Geeft de laatste deployment log terug.

    """

    connection = get_connection()

    if user_id:
        # Haal de laatste log op voor één specifieke gebruiker.
        row = connection.execute(
            """
            SELECT deployment_logs.id, user_id, setup_id, network_setups.name AS setup_name, timestamp, status, output, run_reference, users.username
            FROM deployment_logs
            JOIN users ON users.id = deployment_logs.user_id
            JOIN network_setups ON network_setups.id = deployment_logs.setup_id
            WHERE user_id = ?
            ORDER BY deployment_logs.id DESC
            LIMIT 1
            """,
            (user_id,),
        ).fetchone()

    else:
        # Haal de laatste log op, ongeacht gebruiker.
        row = connection.execute(
            """
            SELECT deployment_logs.id, user_id, setup_id, network_setups.name AS setup_name, timestamp, status, output, run_reference, users.username
            FROM deployment_logs
            JOIN users ON users.id = deployment_logs.user_id
            JOIN network_setups ON network_setups.id = deployment_logs.setup_id
            ORDER BY deployment_logs.id DESC
            LIMIT 1
            """
        ).fetchone()

    connection.close()

    # Als er nog geen logs bestaan, geven we None terug.
    if row is None:
        return None

    # Splits de output in samenvatting en technische output.
    split_output = split_deployment_output(row["output"])

    # Bouw een dictionary voor app.py/templates.
    return {
        "id": row["id"],
        "user_id": row["user_id"],
        "username": row["username"],
        "setup_id": row["setup_id"],
        "setup_name": row["setup_name"],
        "timestamp": row["timestamp"],
        "status": row["status"],
        "output": row["output"],
        "run_reference": row["run_reference"],
        "summary": split_output["summary"],
        "technical_output": split_output["technical_output"],
        "backups": get_backup_files_for_run(row["run_reference"]),
    }


# =====================================================================
# FUNCTIE: get_deployment_logs_for_user(user_id=None, limit=10)
# =====================================================================
def get_deployment_logs_for_user(user_id=None, limit=10):
    """
    Geeft de laatste deployment logs terug.
    """

    connection = get_connection()

    if user_id:
        # Logs van één specifieke gebruiker.
        rows = connection.execute(
            """
            SELECT deployment_logs.id, user_id, setup_id, network_setups.name AS setup_name, timestamp, status, output, run_reference, users.username
            FROM deployment_logs
            JOIN users ON users.id = deployment_logs.user_id
            JOIN network_setups ON network_setups.id = deployment_logs.setup_id
            WHERE user_id = ?
            ORDER BY deployment_logs.id DESC
            LIMIT ?
            """,
            (user_id, limit),
        ).fetchall()

    else:
        # Logs van alle gebruikers.
        rows = connection.execute(
            """
            SELECT deployment_logs.id, user_id, setup_id, network_setups.name AS setup_name, timestamp, status, output, run_reference, users.username
            FROM deployment_logs
            JOIN users ON users.id = deployment_logs.user_id
            JOIN network_setups ON network_setups.id = deployment_logs.setup_id
            ORDER BY deployment_logs.id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    connection.close()

    logs = []

    for row in rows:
        # Splits elke logoutput in een samenvatting en technische output.
        split_output = split_deployment_output(row["output"])

        # Voeg één log toe aan de lijst.
        logs.append({
            "id": row["id"],
            "user_id": row["user_id"],
            "username": row["username"],
            "setup_id": row["setup_id"],
            "setup_name": row["setup_name"],
            "timestamp": row["timestamp"],
            "status": row["status"],
            "output": row["output"],
            "run_reference": row["run_reference"],
            "summary": split_output["summary"],
            "technical_output": split_output["technical_output"],
            "backups": get_backup_files_for_run(row["run_reference"]),
        })

    return logs


# =====================================================================
# FUNCTIE: get_backup_files_for_run(run_reference)
# =====================================================================
def get_backup_files_for_run(run_reference):
    """
    Geeft de backupbestanden terug voor één configuratierun.

    De backups staan in:

        backups/<run_reference>/

    """

    # Als er geen run_reference is, kunnen we geen backupmap bepalen.
    # Dan geven we gewoon een lege lijst terug.
    if not run_reference:
        return []

    # Basismap waarin alle backups staan.
    backup_dir = BASE_DIR / "backups"

    # Map voor deze specifieke run.
    run_backup_dir = backup_dir / run_reference

    # Als de backupmap niet bestaat, zijn er geen backups voor deze run.
    if not run_backup_dir.exists():
        return []

    backup_files = []

    # Overloop alle items in de backupmap.
    for file_path in run_backup_dir.iterdir():
        # We willen enkel echte bestanden tonen.
        # .gitkeep is een leeg bestand dat soms gebruikt wordt om een lege map
        # toch in Git te kunnen bewaren. Dat tonen we niet als echte backup.
        if file_path.is_file() and file_path.name != ".gitkeep":
            backup_files.append({
                # Bestandsnaam zoals die op het dashboard getoond kan worden.
                "name": file_path.name,

                # Relatief pad ten opzichte van de projectroot.
                # Dat is netter dan een volledig absoluut pad van de computer.
                "path": str(file_path.relative_to(BASE_DIR)),

                # Laatste wijzigingstijd van het bestand in Belgische tijd.
                "modified": datetime.fromtimestamp(
                    file_path.stat().st_mtime,
                    ZoneInfo("Europe/Brussels")
                ).strftime("%Y-%m-%d %H:%M:%S"),
            })

    # Sorteer de bestanden op wijzigingsdatum, nieuwste eerst.
    backup_files.sort(key=lambda item: item["modified"], reverse=True)

    return backup_files
