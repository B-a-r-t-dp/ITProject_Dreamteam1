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


def save_deployment_log(user_id, setup_id, status, output):
    """
    Slaat het resultaat van een Ansible-uitvoering op.

    status moet overeenkomen met de koppelafspraken:
    - success
    - failed
    """

    if status not in ("success", "failed"):
        raise ValueError("status moet 'success' of 'failed' zijn")

    connection = get_connection()

    connection.execute(
    """
    INSERT INTO deployment_logs (user_id, setup_id, status, output)
    VALUES (?, ?, ?, ?)
    """,
    (user_id, setup_id, status, output),
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
            SELECT id, user_id, setup_id, timestamp, status, output
            FROM deployment_logs
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (user_id,),
        ).fetchone()

    else:
        row = connection.execute(
            """
            SELECT id, user_id, setup_id, timestamp, status, output
            FROM deployment_logs
            ORDER BY id DESC
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
        "setup_id": row["setup_id"],
        "timestamp": row["timestamp"],
        "status": row["status"],
        "output": row["output"],
        "summary": split_output["summary"],
        "technical_output": split_output["technical_output"],
    }

# def get_last_deployment_log():
#     """
#     Geeft de laatste deployment log terug.

#     app.py gebruikt deze functie om de laatste status/output
#     op het dashboard te tonen.
#     """

#     connection = get_connection()

#     row = connection.execute(
#         """
#         SELECT id, user_id, setup_id, timestamp, status, output
#         FROM deployment_logs
#         ORDER BY id DESC
#         LIMIT 1
#         """
#     ).fetchone()

#     connection.close()

#     if row is None:
#         return None

#     return {
#         "id": row["id"],
#         "user_id": row["user_id"],
#         "setup_id": row["setup_id"],
#         "timestamp": row["timestamp"],
#         "status": row["status"],
#         "output": row["output"],
#     }

def get_deployment_logs_for_user(user_id, limit=10):
    """
    Geeft de laatste deployment logs terug voor één gebruiker/docent.

    Deze functie wordt gebruikt om te controleren welke docent
    welke configuratie gestart heeft.
    """

    connection = get_connection()

    rows = connection.execute(
        """
        SELECT id, user_id, setup_id, timestamp, status, output
        FROM deployment_logs
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (user_id, limit),
    ).fetchall()

    connection.close()

    logs = []

    for row in rows:
        split_output = split_deployment_output(row["output"])

        logs.append({
            "id": row["id"],
            "user_id": row["user_id"],
            "setup_id": row["setup_id"],
            "timestamp": row["timestamp"],
            "status": row["status"],
            "output": row["output"],
            "summary": split_output["summary"],
            "technical_output": split_output["technical_output"],
        })

    return logs
