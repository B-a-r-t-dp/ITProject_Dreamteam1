# Hier komen de SQLite-hulpfuncties.
#
# Verantwoordelijke: Joost
#
# Verwacht:
# - database initialiseren
# - users ophalen/controleren
# - network_setups ophalen
# - deployment_logs opslaan
#
# Vaste koppelafspraken:
# - verander functienamen niet zonder teamoverleg
# - return dictionaries/lijsten zoals beschreven in de docstrings
# - zie docs/koppelafspraken.md


def init_database():
    """
    Maakt de SQLite-database klaar.

    Verantwoordelijke: Joost

    Verwacht gedrag:
    - leest later database/schema.sql in;
    - maakt de tabellen aan als ze nog niet bestaan;
    - zorgt eventueel voor een eerste testdocent en netwerkopstelling.

    Wordt gebruikt door:
    - Lina in app.py bij het opstarten van de Flask-applicatie.

    Return:
    - niets.
    """
    pass


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
    pass


def get_network_setups():
    """
    Geeft de beschikbare netwerkopstellingen terug.

    Verantwoordelijke: Joost

    Verwacht gedrag:
    - leest alle opstellingen uit de tabel network_setups;
    - geeft simpele data terug die Lina direct in het dashboard kan tonen.

    Return:
    [
        {
            "id": 1,
            "name": "Basisopstelling",
            "description": "1 router, 1 switch, HTTP, HTTPS en FTP"
        }
    ]
    """
    pass


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
    pass


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
    pass
