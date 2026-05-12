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
from werkzeug.security import generate_password_hash, check_password_hash


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "data" / "itproject.db"
SCHEMA_PATH = BASE_DIR / "database" / "schema.sql"


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

    connection.execute(
        """
        INSERT OR IGNORE INTO users (username, password_hash, role)
        VALUES (?, ?, ?)
        """,
        ("docent", password_hash, "teacher"),
    )

    connection.execute(
        """
        INSERT OR IGNORE INTO network_setups
        (id, name, description, playbook_data)
        VALUES (?, ?, ?, ?)
        """,
        (
            1,
            "Basisopstelling",
            "1 router, 1 switch, HTTP, HTTPS en FTP",
            "mvp_basis",
        ),
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
        SELECT id, name, description
        FROM network_setups
        ORDER BY id
        """
    ).fetchall()

    connection.close()

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


def get_last_deployment_log():
    """
    Geeft de laatste deployment log terug.

    app.py gebruikt deze functie om de laatste status/output
    op het dashboard te tonen.
    """

    connection = get_connection()

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

    return {
        "id": row["id"],
        "user_id": row["user_id"],
        "setup_id": row["setup_id"],
        "timestamp": row["timestamp"],
        "status": row["status"],
        "output": row["output"],
    }
