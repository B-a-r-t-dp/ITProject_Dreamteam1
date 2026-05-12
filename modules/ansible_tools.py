# Ansible-helper
# Verantwoordelijke: Bart
#
# Dit bestand vormt de brug tussen Flask en Ansible.
#
# Flask hoeft later niet zelf te weten:
# - waar de Ansible-inventory staat;
# - welke playbooks bij een netwerkopstelling horen;
# - hoe ansible-playbook gestart wordt;
# - hoe stdout/stderr verwerkt worden.
#
# Flask roept alleen deze functie aan:
#
# run_setup(setup_id)
#
# Belangrijke koppelafspraak:
# run_setup(setup_id) geeft altijd een dictionary terug met:
#
# {
#     "status": "success" of "failed",
#     "output": "tekstuele output"
# }
#
# Deze vaste structuur is belangrijk omdat:
# - Lina status/output op het dashboard toont;
# - Joost status/output opslaat in SQLite;
# - app.py daardoor simpel en overzichtelijk kan blijven.

from pathlib import Path
import subprocess


# BASE_DIR verwijst naar de hoofdmap van het project.
# Dit werkt ook als het project later op een andere pc staat.
#
# Voorbeeld:
# modules/ansible_tools.py
# -> parent = modules
# -> parent.parent = projectroot
BASE_DIR = Path(__file__).resolve().parent.parent

# Vaste paden naar de Ansible-map, playbooks en inventory.
# Zo moeten we deze paden niet telkens opnieuw hardcoden.
ANSIBLE_DIR = BASE_DIR / "ansible"
PLAYBOOK_DIR = ANSIBLE_DIR / "playbooks"
INVENTORY_PATH = ANSIBLE_DIR / "inventory.ini"


def run_setup(setup_id):
    """
    Start de Ansible-flow voor een gekozen netwerkopstelling.

    Parameters:
    - setup_id: id van de gekozen netwerkopstelling uit SQLite.

    Voor onze MVP gebruiken we voorlopig 1 vaste netwerkopstelling:
    setup_id 1.

    Die basisopstelling bestaat uit:
    - router.yml
    - switch.yml
    - servers.yml

    Return:
    - altijd een dictionary met status en output.

    Voorbeeld bij succes:
    {
        "status": "success",
        "output": "Ansible-output..."
    }

    Voorbeeld bij fout:
    {
        "status": "failed",
        "output": "Foutmelding..."
    }
    """

    playbooks = get_playbooks_for_setup(setup_id)

    # Als er geen playbooks gekoppeld zijn aan deze setup,
    # geven we een duidelijke fout terug in plaats van te crashen.
    if not playbooks:
        return {
            "status": "failed",
            "output": f"Geen Ansible-playbooks gevonden voor setup_id {setup_id}.",
        }

    all_output = []
    has_failed = False

    # We voeren elk playbook apart uit.
    # Zo kunnen we per playbook de output verzamelen.
    for playbook_path in playbooks:
        result = run_playbook(playbook_path)

        all_output.append(f"--- {playbook_path.name} ---")
        all_output.append(result["output"])

        # Als 1 van de playbooks faalt, beschouwen we de volledige flow als failed.
        if result["status"] == "failed":
            has_failed = True

    if has_failed:
        status = "failed"
    else:
        status = "success"

    return {
        "status": status,
        "output": "\n\n".join(all_output),
    }


def get_playbooks_for_setup(setup_id):
    """
    Bepaalt welke playbooks bij een netwerkopstelling horen.

    Voorlopig houden we dit bewust eenvoudig:
    - setup_id 1 is onze MVP-basisopstelling.
    - die start de router-, switch- en serverplaybooks.

    Later kan dit uitgebreid worden op basis van SQLite.
    Bijvoorbeeld met het veld playbook_data uit de tabel network_setups.
    """

    # setup_id kan uit een HTML-formulier komen.
    # Daarom vergelijken we als string, zodat zowel 1 als "1" werkt.
    if str(setup_id) != "1":
        return []

    return [
        PLAYBOOK_DIR / "router.yml",
        PLAYBOOK_DIR / "switch.yml",
        PLAYBOOK_DIR / "servers.yml",
    ]


def run_playbook(playbook_path):
    """
    Start 1 Ansible-playbook met de vaste inventory.

    Deze functie doet de echte subprocess-call naar ansible-playbook.

    Ook hier gebruiken we opnieuw het vaste returnformaat:
    {
        "status": "success" of "failed",
        "output": "..."
    }

    Daardoor blijft run_setup() eenvoudig en voorspelbaar.
    """

    # Controleer eerst of het playbookbestand echt bestaat.
    # Zo krijgen we een duidelijke foutmelding als een pad verkeerd is.
    if not playbook_path.exists():
        return {
            "status": "failed",
            "output": f"Playbook bestaat niet: {playbook_path}",
        }

    # Dit is het commando dat normaal ook manueel in de terminal kan draaien:
    #
    # ansible-playbook -i ansible/inventory.ini ansible/playbooks/router.yml
    #
    # We gebruiken een lijst in plaats van 1 lange string.
    # Dat is veiliger en minder foutgevoelig bij paden met spaties.
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
        # Deze fout betekent meestal dat Ansible niet geïnstalleerd is
        # of dat ansible-playbook niet in PATH staat.
        return {
            "status": "failed",
            "output": "ansible-playbook is niet gevonden. Controleer of Ansible geïnstalleerd is.",
        }

    except Exception as error:
        # Algemene fallback, zodat Flask niet crasht bij een onverwachte fout.
        return {
            "status": "failed",
            "output": f"Onverwachte fout bij starten van Ansible: {error}",
        }

    output_parts = []

    # stdout bevat normale Ansible-output.
    if completed_process.stdout:
        output_parts.append(completed_process.stdout)

    # stderr bevat foutmeldingen of waarschuwingen.
    # We voegen dit ook toe zodat de gebruiker/teamleden kunnen zien wat misging.
    if completed_process.stderr:
        output_parts.append(completed_process.stderr)

    output = "\n".join(output_parts).strip()

    # Soms geeft een commando geen tekst terug.
    # Dan tonen we toch iets begrijpelijks op het dashboard/log.
    if not output:
        output = "Ansible gaf geen output terug."

    # Returncode 0 betekent dat Ansible succesvol klaar was.
    # Alles anders dan 0 behandelen we als failed.
    if completed_process.returncode == 0:
        status = "success"
    else:
        status = "failed"

    return {
        "status": status,
        "output": output,
    }
