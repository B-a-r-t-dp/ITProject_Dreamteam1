# SQLite-hulpfuncties
# Verantwoordelijke: Joost
#
# Dit bestand vormt de brug tussen Flask en SQLite.
#
# app.py hoort geen SQL-query's te bevatten.
# app.py roept alleen functies uit dit bestand aan.
#
# Daardoor blijft de taakverdeling duidelijk:
# - Lina: Flask-routes, sessies en templates
# - Joost: database, tabellen, users, setups en logs
# - Bart: Ansible en Docker

import sqlite3
from pathlib import Path
import yaml
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime
from zoneinfo import ZoneInfo


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "data" / "itproject.db"
SCHEMA_PATH = BASE_DIR / "database" / "schema.sql"
PLAYBOOK_DIR = BASE_DIR / "ansible" / "playbooks"


def get_connection():
    """
    Maakt verbinding met de SQLite-database.

    De database staat bewust in de map data/.
    Daardoor blijft app.py weg van rechtstreekse databasepaden.
    """

    DATABASE_PATH.parent.mkdir(exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def init_database():
    """
    Initialiseert de database.

    Deze functie:
    - maakt tabellen aan vanuit database/schema.sql;
    - maakt een testdocent aan;
    - maakt 1 basisnetwerkopstelling aan voor de MVP.

    Daardoor kan de app na het opstarten meteen getest worden.
    """

    connection = get_connection()

    with open(SCHEMA_PATH, "r", encoding="utf-8") as schema_file:
        schema_sql = schema_file.read()

    connection.executescript(schema_sql)

    # Bestaande databases krijgen deze kolom niet automatisch via schema.sql.
    # Daarom voegen we ze hier veilig toe als ze nog ontbreekt.
    try:
        connection.execute("ALTER TABLE deployment_logs ADD COLUMN run_reference TEXT")
    except sqlite3.OperationalError:
        pass

    password_hash = generate_password_hash("docent123")

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

    connection.executemany(
        """
        INSERT OR IGNORE INTO network_setups
        (id, name, description, playbook_data)
        VALUES (?, ?, ?, ?)
        """,
        network_setups,
    )

    connection.executemany(
        """
        UPDATE network_setups
        SET name = ?, description = ?, playbook_data = ?
        WHERE id = ?
        """,
        [
            (setup[1], setup[2], setup[3], setup[0])
            for setup in network_setups
        ],
    )

    connection.commit()
    connection.close()


def verify_user(username, password):
    """
    Controleert of een gebruiker mag aanmelden.

    Return bij correcte login:
    {
        "id": 1,
        "username": "docent",
        "role": "teacher"
    }

    Return bij fout:
    None
    """

    if not username or not password:
        return None

    connection = get_connection()

    user = connection.execute(
        """
        SELECT id, username, password_hash, role
        FROM users
        WHERE username = ?
        """,
        (username,),
    ).fetchone()

    connection.close()

    if user is None:
        return None

    if not check_password_hash(user["password_hash"], password):
        return None

    return {
        "id": user["id"],
        "username": user["username"],
        "role": user["role"],
    }


def get_network_setups():
    """
    Haalt alle beschikbare netwerkopstellingen op.

    app.py gebruikt deze functie om het dashboard te vullen.
    """

    connection = get_connection()

    rows = connection.execute(
        """
        SELECT id, name, description, playbook_data
        FROM network_setups
        ORDER BY id
        """
    ).fetchall()

    connection.close()

    network_setups = []

    for row in rows:
        setup_info = get_setup_info(row["playbook_data"])

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


def get_setup_info(setup_folder):
    """
    Leest extra informatie over een netwerkopstelling.

    De playbooks voeren de configuratie uit.
    info.yml beschrijft in mensentaal wat die opstelling doet,
    zodat het dashboard dit kan tonen zonder hardcoded HTML.
    """

    info_path = PLAYBOOK_DIR / setup_folder / "info.yml"

    if not info_path.exists():
        return None

    with open(info_path, "r", encoding="utf-8") as info_file:
        return yaml.safe_load(info_file)


# def save_deployment_log(user_id, setup_id, status, output):
#     """
#     Slaat het resultaat van een Ansible-uitvoering op.

#     status moet overeenkomen met de koppelafspraken:
#     - success
#     - failed
#     """

#     if status not in ("success", "failed"):
#         raise ValueError("status moet 'success' of 'failed' zijn")

#     connection = get_connection()

#     connection.execute(
#     """
#     INSERT INTO deployment_logs (user_id, setup_id, status, output)
#     VALUES (?, ?, ?, ?)
#     """,
#     (user_id, setup_id, status, output),
# )

#     connection.commit()
#     connection.close()

def save_deployment_log(user_id, setup_id, status, output, run_reference=None):
    """
    Slaat het resultaat van een Ansible-uitvoering op.
    De timestamp wordt bewust in Belgische tijd opgeslagen.

    run_reference koppelt deze log aan de juiste backupmap.
    """

    if status not in ("success", "failed"):
        raise ValueError("status moet 'success' of 'failed' zijn")

    belgian_time = datetime.now(ZoneInfo("Europe/Brussels")).strftime("%Y-%m-%d %H:%M:%S")

    connection = get_connection()

    connection.execute(
        """
        INSERT INTO deployment_logs (user_id, setup_id, timestamp, status, output, run_reference)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (user_id, setup_id, belgian_time, status, output, run_reference),
    )

    connection.commit()
    connection.close()


def split_deployment_output(output):
    """
    Splitst de Ansible-output in 2 stukken:
    - een korte samenvatting;
    - de technische output.

    ansible_tools.py zet bewust "TECHNISCHE OUTPUT" tussen die delen.
    Zo blijft deze functie simpel en moet dashboard.html geen moeilijke
    tekstlogica doen.
    """

    marker = "TECHNISCHE OUTPUT"

    if not output or marker not in output:
        return {
            "summary": output,
            "technical_output": "",
        }

    summary, technical_output = output.split(marker, 1)

    summary = summary.replace("SAMENVATTING CONFIGURATIE", "").strip()
    technical_output = technical_output.strip()

    return {
        "summary": summary,
        "technical_output": technical_output,
    }


def get_last_deployment_log(user_id=None):
    """
    Geeft de laatste deployment log terug.

    Indien user_id meegegeven wordt,
    krijgt de gebruiker enkel zijn eigen logs te zien.
    """

    connection = get_connection()

    if user_id:
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

    if row is None:
        return None

    split_output = split_deployment_output(row["output"])

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


def get_deployment_logs_for_user(user_id=None, limit=10):
    """
    Geeft de laatste deployment logs terug.

    Als user_id meegegeven wordt, tonen we enkel die gebruiker.
    Als user_id leeg blijft, tonen we alle gebruikers.
    """

    connection = get_connection()

    if user_id:
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
        split_output = split_deployment_output(row["output"])

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


def get_backup_files_for_run(run_reference):
    """
    Geeft de backupbestanden terug voor 1 configuratierun.

    De backups staan in:
    backups/<run_reference>/

    Zo blijven backups gekoppeld aan de juiste geschiedenisregel.
    """

    if not run_reference:
        return []

    backup_dir = BASE_DIR / "backups"
    run_backup_dir = backup_dir / run_reference

    if not run_backup_dir.exists():
        return []

    backup_files = []

    for file_path in run_backup_dir.iterdir():
        if file_path.is_file() and file_path.name != ".gitkeep":
            backup_files.append({
                "name": file_path.name,
                "path": str(file_path.relative_to(BASE_DIR)),
                "modified": datetime.fromtimestamp(
                    file_path.stat().st_mtime,
                    ZoneInfo("Europe/Brussels")
                ).strftime("%Y-%m-%d %H:%M:%S"),
            })

    backup_files.sort(key=lambda item: item["modified"], reverse=True)

    return backup_files



