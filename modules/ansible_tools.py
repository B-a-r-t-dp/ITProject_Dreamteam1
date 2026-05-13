# Ansible-helper
# Verantwoordelijke: Bart
#
# Dit bestand vormt de brug tussen Flask en Ansible.
#
# Flask roept later alleen run_setup(setup_id) aan.
# Alle Ansible-logica blijft dus in dit bestand.
#
# Belangrijke koppelafspraak:
# run_setup(setup_id) geeft altijd een dictionary terug met:
#
# {
#     "status": "success" of "failed",
#     "output": "tekstuele output"
# }
#
# Daardoor kan app.py de status/output tonen of doorgeven
# aan database_tools.py om op te slaan in SQLite.

from pathlib import Path
import subprocess


BASE_DIR = Path(__file__).resolve().parent.parent
ANSIBLE_DIR = BASE_DIR / "ansible"
PLAYBOOK_DIR = ANSIBLE_DIR / "playbooks"
INVENTORY_PATH = ANSIBLE_DIR / "inventory.ini"


def run_setup(setup_id):
    """
    Start de Ansible-flow voor een gekozen netwerkopstelling.

    Voor de MVP gebruiken we voorlopig setup_id 1.
    Die start:
    - ansible/playbooks/setup1/router.yml
    - ansible/playbooks/setup1/switch.yml
    - ansible/playbooks/setup1/servers.yml

    Return:
    - altijd {"status": "...", "output": "..."}
    """

    playbooks = get_playbooks_for_setup(setup_id)

    if not playbooks:
        return {
            "status": "failed",
            "output": f"Geen Ansible-playbooks gevonden voor setup_id {setup_id}.",
        }

    all_output = []
    has_failed = False

    for playbook_path in playbooks:
        result = run_playbook(playbook_path)

        all_output.append(f"--- {playbook_path.name} ---")
        all_output.append(result["output"])

        if result["status"] == "failed":
            has_failed = True

    status = "failed" if has_failed else "success"

    return {
        "status": status,
        "output": "\n\n".join(all_output),
    }


def get_playbooks_for_setup(setup_id):
    """
    Koppelt een setup_id aan de juiste playbooks.

    Voorlopig is setup_id 1 gekoppeld aan de map setup1.
    Later kan dit uitgebreid worden met data uit SQLite,
    bijvoorbeeld via het veld playbook_data.
    """

    setup_folders = {
        "1": "setup1",
    }

    setup_folder = setup_folders.get(str(setup_id))

    if setup_folder is None:
        return []

    setup_path = PLAYBOOK_DIR / setup_folder

    return [
        setup_path / "router.yml",
        setup_path / "switch.yml",
        setup_path / "servers.yml",
    ]


def run_playbook(playbook_path):
    """
    Start 1 Ansible-playbook met de vaste inventory.

    Deze functie vangt fouten op en zet alles om naar
    het vaste status/output-formaat.
    """

    if not playbook_path.exists():
        return {
            "status": "failed",
            "output": f"Playbook bestaat niet: {playbook_path}",
        }

    command = [
        "ansible-playbook",
        "-i",
        str(INVENTORY_PATH),
        str(playbook_path),
    ]

    try:
        completed_process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            cwd=BASE_DIR,
        )

    except FileNotFoundError:
        return {
            "status": "failed",
            "output": "ansible-playbook is niet gevonden. Controleer of Ansible geinstalleerd is.",
        }

    except Exception as error:
        return {
            "status": "failed",
            "output": f"Onverwachte fout bij starten van Ansible: {error}",
        }

    output_parts = []

    if completed_process.stdout:
        output_parts.append(completed_process.stdout)

    if completed_process.stderr:
        output_parts.append(completed_process.stderr)

    output = "\n".join(output_parts).strip()

    if not output:
        output = "Ansible gaf geen output terug."

    status = "success" if completed_process.returncode == 0 else "failed"

    return {
        "status": status,
        "output": output,
    }
