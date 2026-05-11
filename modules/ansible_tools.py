# Hier komen de functies om Ansible vanuit Flask te starten.
#
# Verantwoordelijke: Bart
#
# Verwacht:
# - gekozen netwerkopstelling ontvangen
# - juiste playbook starten
# - status en output teruggeven
#
# Vaste koppelafspraak:
# - run_setup(setup_id) geeft altijd een dict terug met status en output
# - verander deze sleutels niet zonder teamoverleg
# - zie docs/koppelafspraken.md


def run_setup(setup_id):
    """
    Start de Ansible-flow voor een gekozen netwerkopstelling.

    Verantwoordelijke: Bart

    Parameters:
    - setup_id: id van de netwerkopstelling uit SQLite.

    Verwacht gedrag:
    - bepaalt welk playbook of welke playbooks gestart moeten worden;
    - start later Ansible via subprocess of een andere duidelijke methode;
    - verzamelt stdout/stderr van Ansible;
    - geeft altijd hetzelfde outputformaat terug.

    Return bij succes:
    {
        "status": "success",
        "output": "Ansible-output..."
    }

    Return bij fout:
    {
        "status": "failed",
        "output": "Foutmelding..."
    }

    Belangrijke afspraak:
    - Lina mag in app.py vertrouwen op deze exacte sleutels: status en output.
    - Joost slaat status en output op in deployment_logs.
    """
    return {
        "status": "failed",
        "output": "TODO: run_setup is nog niet geimplementeerd.",
    }
