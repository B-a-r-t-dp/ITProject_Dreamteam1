# Ansible-helper
# Verantwoordelijke: Bart
#
# Dit bestand vormt de brug tussen Flask en Ansible.
#
# app.py roept alleen run_setup(setup_id) aan.
# Alle echte Ansible-logica blijft dus in dit bestand.

import os                       # Wordt gebruikt om paden te maken die op elke pc werken.
import subprocess               # Wordt gebruikt om ansible-playbook vanuit Python te starten.



###############################################################################
#                              Path variabelen                                #
###############################################################################

# We bouwen de paden op vanaf de projectmap.
# Zo werkt dit bestand ook als de projectmap bij iemand anders anders noemt.

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANSIBLE_DIR = os.path.join(BASE_DIR, "ansible")
PLAYBOOK_DIR = os.path.join(ANSIBLE_DIR, "playbooks")

# Algemene inventory blijft als fallback bestaan.
# Als een setup eigen inventory.ini heeft, gebruiken we die.
ALGEMENE_INVENTORY = os.path.join(ANSIBLE_DIR, "inventory.ini")



###############################################################################
#                         Functies opstart Ansible                            #
###############################################################################


def run_setup(setup_id, logged_user=None):
    """
    Start de Ansible-flow voor een gekozen netwerkopstelling.

    logged_user is de username van de ingelogde docent.
    Die naam gebruiken we in de backupbestanden van router en switch.
    """

    setup_info = get_setup_info(setup_id)        # Setupinfo opvragen volgens setup_id.

    if setup_info == None:
        setup_info_status = {
            "status": "failed",
            "output": "Geen geldige setup gevonden voor setup_id " + str(setup_id),
        }
        return setup_info_status

    playbooks = get_playbooks_for_setup(setup_info)  # Playbooks opvragen volgens de setupinfo.

    if not playbooks:
        playbooks_status = {
            "status": "failed",
            "output": "Geen Ansible-playbooks gevonden voor setup_id " + str(setup_id),
        }
        return playbooks_status

    samenvatting_regels = []
    technische_output = []

    # Deze variabele onthoudt of minstens 1 playbook gefaald is.
    # Zo kan de volledige setup op failed gezet worden.
    er_is_een_fout = False

    for playbook_pad in playbooks:
        playbook_naam = os.path.basename(playbook_pad)

        ansible_resultaat = run_playbook(playbook_pad, setup_info["inventory"], logged_user)

        if ansible_resultaat["status"] == "success":
            samenvatting_regels.append("[OK] " + playbook_naam + " is succesvol uitgevoerd.")

        else:
            er_is_een_fout = True
            samenvatting_regels.append("[FOUT] " + playbook_naam + " is mislukt.")
            samenvatting_regels.append("Mogelijke oorzaak: " + explain_ansible_error(ansible_resultaat["output"]))

        # De technische output bewaren we apart.
        # Die wordt later openklapbaar getoond op het dashboard.
        technische_output.append("--- " + playbook_naam + " ---")
        technische_output.append(ansible_resultaat["output"])

    if er_is_een_fout:
        ansible_status = "failed"
    else:
        ansible_status = "success"

    ansible_output = maak_volledige_output(samenvatting_regels, technische_output)

    ansible_log = {
        "status": ansible_status,
        "output": ansible_output,
    }

    return ansible_log


def get_setup_info(setup_id):
    """
    Zoekt welke setupmap en inventory bij een setup horen.

    setup_id 1 is gelinkt aan map setup1.
    setup_id 2 is gelinkt aan map setup2.

    Als een setup een eigen inventory.ini heeft, gebruiken we die.
    Anders gebruiken we de algemene inventory als fallback.
    """

    setup_map_naam = "setup" + str(setup_id)

    # Volledig pad naar de setupmap.
    # Bijvoorbeeld: ansible/playbooks/setup1
    setup_pad = os.path.join(PLAYBOOK_DIR, setup_map_naam)

    # Als de setupmap niet bestaat, kan deze setup niet uitgevoerd worden.
    if not os.path.isdir(setup_pad):
        return None

    # Eerst kijken we of de setup een eigen inventory heeft.
    eigen_inventory = os.path.join(setup_pad, "inventory.ini")

    if os.path.exists(eigen_inventory):
        inventory_pad = eigen_inventory
    else:
        inventory_pad = ALGEMENE_INVENTORY

    setup_info = {
        "id": setup_id,
        "map_naam": setup_map_naam,
        "pad": setup_pad,
        "inventory": inventory_pad,
    }

    return setup_info


def get_playbooks_for_setup(setup_info):
    """
    Geeft de playbooks terug die bij een setup horen.
    Alleen playbooks die echt bestaan worden uitgevoerd.
    """

    setup_pad = setup_info["pad"]

    # Dit zijn de playbooks die we verwachten in elke setupmap.
    # In de MVP houden we dit bewust hardcoded.
    mogelijke_playbooks = [
        os.path.join(setup_pad, "router.yml"),
        os.path.join(setup_pad, "switch.yml"),
        os.path.join(setup_pad, "servers.yml"),
    ]

    bestaande_playbooks = []

    for playbook_pad in mogelijke_playbooks:
        if os.path.exists(playbook_pad):
            bestaande_playbooks.append(playbook_pad)

    return bestaande_playbooks


def run_playbook(playbook_pad, inventory_pad, logged_user=None):
    """
    Start 1 Ansible-playbook.
    Deze functie wordt per playbook opgeroepen vanuit run_setup().
    """

    if not os.path.exists(playbook_pad):
        playbook_status = {
            "status": "failed",
            "output": "Playbook bestaat niet: " + playbook_pad,
        }
        return playbook_status

    if not os.path.exists(inventory_pad):
        inventory_status = {
            "status": "failed",
            "output": "Inventory bestaat niet: " + inventory_pad,
        }
        return inventory_status

    # Dit is het terminalcommando dat Python straks uitvoert.
    # Bijvoorbeeld: ansible-playbook -i inventory.ini router.yml
    command = [
        "ansible-playbook",
        "-i",
        inventory_pad,
        playbook_pad,
    ]

    if logged_user:
        # De ingelogde gebruiker wordt meegegeven aan Ansible.
        # Die naam wordt gebruikt in de backupbestanden.
        command.append("-e")
        command.append("logged_user=" + logged_user)

    try:
        # Hier doen we een poging om het Ansible-commando te starten.
        uitgevoerd_proces = subprocess.run(
            command,
            capture_output=True,       # Vangt de output en foutmeldingen op in Python.
            text=True,                 # Zorgt dat de output gewone tekst is en geen bytes.
            cwd=BASE_DIR,              # Voert het commando uit vanaf de projectmap.
        )

    except FileNotFoundError:
        # Deze fout betekent dat het programma ansible-playbook zelf niet gevonden is.
        ansible_foutvertaling_file_not_found = {
            "status": "failed",
            "output": "ansible-playbook is niet gevonden. Controleer of Ansible geinstalleerd is.",
        }
        return ansible_foutvertaling_file_not_found

    except Exception as fout:
        # Algemene opvang voor fouten die we niet apart voorzien hebben.
        # str(fout) zet de technische fout om naar tekst.
        ansible_foutvertaling_onverwachte_fout = {
            "status": "failed",
            "output": "Onverwachte fout bij starten van Ansible: " + str(fout),
        }
        return ansible_foutvertaling_onverwachte_fout

    ansible_output = maak_technische_output(uitgevoerd_proces)

    # returncode 0 betekent dat het terminalcommando succesvol uitgevoerd is.
    # Alles anders dan 0 behandelen we als failed.
    if uitgevoerd_proces.returncode == 0:
        ansible_status = "success"
    else:
        ansible_status = "failed"

    ansible_log = {
        "status": ansible_status,
        "output": ansible_output,
    }

    return ansible_log



###############################################################################
#                         Functies output Ansible                             #
###############################################################################


def maak_technische_output(uitgevoerd_proces):
    """
    Zet stdout en stderr van Ansible om naar tekst.

    stdout = gewone Ansible-output
    stderr = waarschuwingen of foutdetails
    """

    output_delen = []

    if uitgevoerd_proces.stdout:
        output_delen.append("ANSIBLE OUTPUT")
        output_delen.append("")
        output_delen.append(uitgevoerd_proces.stdout)

    if uitgevoerd_proces.stderr:
        output_delen.append("WAARSCHUWINGEN / FOUTDETAILS")
        output_delen.append("")
        output_delen.append(uitgevoerd_proces.stderr)

    output = "\n".join(output_delen).strip()

    if output == "":
        output = "Ansible gaf geen output terug."

    return output


def maak_volledige_output(samenvatting_regels, technische_output):
    """
    Maakt de volledige output die opgeslagen wordt in SQLite.

    database_tools.py gebruikt de tekst 'TECHNISCHE OUTPUT'
    om de samenvatting en technische output later te splitsen.
    Die tekst dus niet zomaar aanpassen.
    """

    volledige_output = []

    volledige_output.append("SAMENVATTING CONFIGURATIE")
    volledige_output.append("")
    volledige_output.extend(samenvatting_regels)
    volledige_output.append("")
    volledige_output.append("TECHNISCHE OUTPUT")
    volledige_output.append("")
    volledige_output.extend(technische_output)

    return "\n\n".join(volledige_output)


def explain_ansible_error(output):
    """
    Geeft een korte uitleg bij bekende Ansible-fouten.

    We gebruiken bewust gewone if-statements.
    Dat is makkelijker te lezen en uit te leggen dan regex.
    """

    output_lower = output.lower()

    if "authentication failed" in output_lower or "failed to authenticate" in output_lower:
        return "de login of het enable-wachtwoord klopt waarschijnlijk niet."

    if "timed out" in output_lower or "timeout" in output_lower:
        return "het toestel is offline, reageerde te traag of bleef hangen tijdens een commando."

    if "unreachable" in output_lower:
        return "het toestel is niet bereikbaar via het netwerk."

    if "connection refused" in output_lower:
        return "de service of SSH staat waarschijnlijk niet actief."

    if "no route to host" in output_lower:
        return "het IP-adres is niet bereikbaar vanaf de Flask-container."

    if "no acceptable kex algorithm" in output_lower or "no matching key exchange" in output_lower:
        return "de SSH-instellingen passen niet bij het Cisco/EVE-NG-toestel."

    if "name does not resolve" in output_lower:
        return "een Docker-servicenaam kon niet gevonden worden."

    if "status code was" in output_lower:
        return "een HTTP- of HTTPS-check kreeg niet de verwachte status 200."

    if "assertionerror" in output_lower or "test.txt" in output_lower:
        return "de FTP-login werkte mogelijk, maar het testbestand werd niet gevonden."

    if "docker" in output_lower and "non-zero return code" in output_lower:
        return "Docker Compose gaf een fout terug bij het starten of controleren van een container."

    return "bekijk de technische output hieronder voor de exacte fout."
