# Ansible-helper
# Verantwoordelijke: Bart
#
# Dit bestand vormt de brug tussen Flask en Ansible.
#
# app.py roept functies uit dit bestand aan voor:
# - setupwaarden valideren en opslaan;
# - Ansible starten.
# Alle echte Ansible-logica blijft dus hier.

import os                       # Wordt gebruikt om paden te maken die op elke pc werken.
import subprocess               # Wordt gebruikt om ansible-playbook vanuit Python te starten.
import copy                     # Wordt gebruikt om de setupdata veilig te kopiëren.
import yaml                     # Wordt gebruikt om info.yml te lezen.
import ipaddress

###############################################################################
#                              Path variabelen                                #
###############################################################################

# We bouwen de paden op vanaf de projectmap.
# Zo werkt dit bestand ook als de projectmap bij iemand anders anders noemt.

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANSIBLE_DIR = os.path.join(BASE_DIR, "ansible")
PLAYBOOK_DIR = os.path.join(ANSIBLE_DIR, "playbooks")

def validate_custom_variables(setup_id, custom_variables):
    """
    Controleert de formulierwaarden voordat Ansible gestart wordt.

    We houden de controles bewust simpel en leesbaar:
    - verplichte velden mogen niet leeg zijn;
    - IP-adressen moeten echte IP-adressen zijn;
    - VLANs moeten tussen 1 en 4094 liggen;
    - interfaces mogen geen spaties bevatten.
    """

    errors = []

    def check_required(field_name, label):
        value = custom_variables.get(field_name, "").strip()

        if value == "":
            errors.append(label + " mag niet leeg zijn.")

        return value

    def check_ip(field_name, label):
        value = custom_variables.get(field_name, "").strip()

        if value == "":
            errors.append(label + " mag niet leeg zijn.")
            return

        try:
            ipaddress.ip_address(value)
        except ValueError:
            errors.append(label + " moet een geldig IP-adres zijn.")

    def check_vlan(field_name, label):
        value = custom_variables.get(field_name, "").strip()

        if value == "":
            errors.append(label + " mag niet leeg zijn.")
            return

        if not value.isdigit():
            errors.append(label + " moet een getal zijn.")
            return

        vlan_id = int(value)

        if vlan_id < 1 or vlan_id > 4094:
            errors.append(label + " moet tussen 1 en 4094 liggen.")

    def check_vlan_list(field_name, label):
        value = custom_variables.get(field_name, "").strip()

        if value == "":
            errors.append(label + " mag niet leeg zijn.")
            return

        vlan_values = value.split(",")

        for vlan in vlan_values:
            vlan = vlan.strip()

            if not vlan.isdigit():
                errors.append(label + " mag alleen VLAN-nummers bevatten, gescheiden door komma's.")
                return

            vlan_id = int(vlan)

            if vlan_id < 1 or vlan_id > 4094:
                errors.append(label + " bevat een VLAN buiten bereik 1-4094.")
                return

    def check_interface(field_name, label):
        value = custom_variables.get(field_name, "").strip()

        if value == "":
            errors.append(label + " mag niet leeg zijn.")
            return

        if " " in value:
            errors.append(label + " mag geen spaties bevatten.")

    def check_number(field_name, label, minimum, maximum):
        value = custom_variables.get(field_name, "").strip()

        if value == "":
            errors.append(label + " mag niet leeg zijn.")
            return

        if not value.isdigit():
            errors.append(label + " moet een getal zijn.")
            return

        number = int(value)

        if number < minimum or number > maximum:
            errors.append(label + " moet tussen " + str(minimum) + " en " + str(maximum) + " liggen.")

    setup_id = str(setup_id)

    if setup_id == "1":
        check_required("router_hostname", "Router hostname")
        check_ip("router_management_ip", "Router management-IP")
        check_interface("router_lab_interface", "Router labinterface")
        check_required("router_lab_description", "Router labinterface beschrijving")
        check_ip("router_lab_ip", "Router lab IP-adres")
        check_ip("router_lab_mask", "Router lab subnetmasker")
        check_number("router_ospf_process", "OSPF process", 1, 65535)
        check_ip("router_ospf_router_id", "OSPF router-id")
        check_ip("router_ospf_network", "OSPF netwerk")
        check_ip("router_ospf_wildcard", "OSPF wildcard")
        check_number("router_ospf_area", "OSPF area", 0, 4294967295)

        check_required("switch_hostname", "Switch hostname")
        check_ip("switch_management_ip", "Switch management-IP")
        check_interface("switch_access_port", "Switch accesspoort")
        check_required("switch_access_description", "Switch accesspoort beschrijving")
        check_vlan("switch_access_vlan", "Switch access VLAN")
        check_interface("switch_trunk_port", "Switch trunkpoort")
        check_required("switch_trunk_description", "Switch trunk beschrijving")
        check_vlan_list("switch_trunk_allowed_vlans", "Toegelaten VLANs op trunk")

        for field_name in sorted(custom_variables.keys()):
            if field_name.startswith("setup1_vlan_") and field_name.endswith("_id"):
                vlan_index = field_name.replace("setup1_vlan_", "").replace("_id", "")
                check_vlan(field_name, "VLAN " + vlan_index + " nummer")

            if field_name.startswith("setup1_vlan_") and field_name.endswith("_name"):
                vlan_index = field_name.replace("setup1_vlan_", "").replace("_name", "")
                check_required(field_name, "VLAN " + vlan_index + " naam")

    if setup_id == "2":
        check_required("router_hostname", "Router hostname")
        check_ip("router_management_ip", "Router management-IP")
        check_interface("router_trunk_interface", "Router trunkinterface")
        check_required("router_trunk_description", "Router trunk beschrijving")

        for field_name in sorted(custom_variables.keys()):
            if field_name.startswith("setup2_subinterface_") and field_name.endswith("_vlan"):
                check_vlan(field_name, field_name.replace("_", " "))

            if field_name.startswith("setup2_subinterface_") and field_name.endswith("_description"):
                check_required(field_name, field_name.replace("_", " "))

            if field_name.startswith("setup2_subinterface_") and field_name.endswith("_ip"):
                check_ip(field_name, field_name.replace("_", " "))

            if field_name.startswith("setup2_subinterface_") and field_name.endswith("_mask"):
                check_ip(field_name, field_name.replace("_", " "))

            if field_name.startswith("setup2_vlan_") and field_name.endswith("_id"):
                check_vlan(field_name, field_name.replace("_", " "))

            if field_name.startswith("setup2_vlan_") and field_name.endswith("_name"):
                check_required(field_name, field_name.replace("_", " "))

        for switch_name in ["sw11", "sw12", "distsw", "classsw"]:
            check_required(switch_name + "_hostname", switch_name.upper() + " hostname")
            check_ip(switch_name + "_management_ip", switch_name.upper() + " management-IP")

        for field_name in sorted(custom_variables.keys()):
            if field_name.startswith(("sw11_trunk_", "sw12_trunk_", "distsw_trunk_", "classsw_trunk_")):
                if field_name.endswith("_interface"):
                    check_interface(field_name, field_name.replace("_", " "))

                if field_name.endswith("_description"):
                    check_required(field_name, field_name.replace("_", " "))

            if field_name.startswith(("distsw_etherchannel_", "classsw_etherchannel_")):
                if field_name.endswith("_port_channel"):
                    check_number(field_name, field_name.replace("_", " "), 1, 64)

                if field_name.endswith("_mode"):
                    value = custom_variables.get(field_name, "").strip()

                    if value == "":
                        errors.append(field_name.replace("_", " ") + " mag niet leeg zijn.")

                    if value not in ["active", "passive", "on"]:
                        errors.append(field_name.replace("_", " ") + " moet active, passive of on zijn.")

                if field_name.endswith("_interface"):
                    check_interface(field_name, field_name.replace("_", " "))

                if field_name.endswith("_description"):
                    check_required(field_name, field_name.replace("_", " "))

            if field_name.startswith("classsw_access_"):
                if field_name.endswith("_interface"):
                    check_interface(field_name, field_name.replace("_", " "))

                if field_name.endswith("_description"):
                    check_required(field_name, field_name.replace("_", " "))

                if field_name.endswith("_vlan"):
                    check_vlan(field_name, field_name.replace("_", " "))

        check_vlan_list("switches_trunk_allowed_vlans", "Toegelaten VLANs op trunks")

    return errors

###############################################################################
#                         Functies opstart Ansible                            #
###############################################################################


def run_setup(setup_id, logged_user=None, run_reference=None):
    """
    Start de Ansible-flow voor een gekozen netwerkopstelling.

    logged_user is de username van de ingelogde docent.
    Die naam gebruiken we in de backupbestanden van router en switch.

    run_reference is de unieke naam van deze configuratierun.
    Die gebruiken we als backupmap.
    """

    setup_info = get_setup_info(setup_id)        # Setupinfo opvragen volgens setup_id.

    if setup_info == None:
        setup_info_status = {
            "status": "failed",
            "output": "Geen geldige setup gevonden voor setup_id " + str(setup_id),
        }
        return setup_info_status

    playbooks = get_playbooks_for_setup(setup_info)  # Playbooks opvragen volgens de setupinfo.
    runtime_variables = build_runtime_variables(setup_info)
    runtime_inventory = maak_runtime_inventory(setup_info, runtime_variables, run_reference)

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

        ansible_resultaat = run_playbook(
            playbook_pad,
            runtime_inventory,
            logged_user,
            run_reference,
        )

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

    Elke setup moet een eigen inventory.ini hebben.
    Zo blijven de IP-adressen per netwerkopstelling duidelijk gescheiden.
    """

    setup_map_naam = "setup" + str(setup_id)

    # Volledig pad naar de setupmap.
    # Bijvoorbeeld: ansible/playbooks/setup1
    setup_pad = os.path.join(PLAYBOOK_DIR, setup_map_naam)

    # Als de setupmap niet bestaat, kan deze setup niet uitgevoerd worden.
    if not os.path.isdir(setup_pad):
        return None

    # Elke setup heeft bewust een eigen inventory.
    # Als die ontbreekt, voeren we de setup niet uit.
    inventory_pad = os.path.join(setup_pad, "inventory.ini")

    if not os.path.exists(inventory_pad):
        return None

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


def build_runtime_variables(setup_info, custom_variables=None):
    """
    Bouwt de variabelen op die naar Ansible gestuurd worden.

    We vertrekken altijd van info.yml.
    Daarna overschrijven we de waarden die de docent in het formulier invult.

    Deze functie schrijft zelf nog niets weg.
    update_setup_info_file() gebruikt deze data om info.yml te bewaren.
    """

    info_pad = os.path.join(setup_info["pad"], "info.yml")

    with open(info_pad, "r", encoding="utf-8") as info_file:
        info_data = yaml.safe_load(info_file)

    runtime_data = copy.deepcopy(info_data)

    if not custom_variables:
        return runtime_data

    setup_id = str(setup_info["id"])
    variables = runtime_data.get("variables", {})

    if setup_id == "1":
        router = variables.get("router", {})
        switch = variables.get("switch", {})

        router["hostname"] = custom_variables.get("router_hostname", router.get("hostname"))
        router["management_ip"] = custom_variables.get("router_management_ip", router.get("management_ip"))
        router["lab_interface"] = custom_variables.get("router_lab_interface", router.get("lab_interface"))
        router["lab_description"] = custom_variables.get("router_lab_description", router.get("lab_description"))
        router["lab_ip"] = custom_variables.get("router_lab_ip", router.get("lab_ip"))
        router["lab_mask"] = custom_variables.get("router_lab_mask", router.get("lab_mask"))
        router["ospf_process"] = custom_variables.get("router_ospf_process", router.get("ospf_process"))
        router["ospf_router_id"] = custom_variables.get("router_ospf_router_id", router.get("ospf_router_id"))
        router["ospf_network"] = custom_variables.get("router_ospf_network", router.get("ospf_network"))
        router["ospf_wildcard"] = custom_variables.get("router_ospf_wildcard", router.get("ospf_wildcard"))
        router["ospf_area"] = custom_variables.get("router_ospf_area", router.get("ospf_area"))

        switch["hostname"] = custom_variables.get("switch_hostname", switch.get("hostname"))
        switch["management_ip"] = custom_variables.get("switch_management_ip", switch.get("management_ip"))
        switch["access_port"] = custom_variables.get("switch_access_port", switch.get("access_port"))
        switch["access_description"] = custom_variables.get("switch_access_description", switch.get("access_description"))
        switch["access_vlan"] = custom_variables.get("switch_access_vlan", switch.get("access_vlan"))
        switch["trunk_port"] = custom_variables.get("switch_trunk_port", switch.get("trunk_port"))
        switch["trunk_description"] = custom_variables.get("switch_trunk_description", switch.get("trunk_description"))
        switch["trunk_allowed_vlans"] = custom_variables.get("switch_trunk_allowed_vlans", switch.get("trunk_allowed_vlans"))

        vlans = switch.get("vlans", [])

        for index, vlan in enumerate(vlans):
            vlan["id"] = custom_variables.get("setup1_vlan_" + str(index) + "_id", vlan.get("id"))
            vlan["name"] = custom_variables.get("setup1_vlan_" + str(index) + "_name", vlan.get("name"))

    if setup_id == "2":
        router = variables.get("router", {})
        vlans = variables.get("vlans", [])
        switches = variables.get("switches", {})

        router["hostname"] = custom_variables.get("router_hostname", router.get("hostname"))
        router["management_ip"] = custom_variables.get("router_management_ip", router.get("management_ip"))
        router["trunk_interface"] = custom_variables.get("router_trunk_interface", router.get("trunk_interface"))
        router["trunk_description"] = custom_variables.get("router_trunk_description", router.get("trunk_description"))

        subinterfaces = router.get("subinterfaces", [])

        for index, subinterface in enumerate(subinterfaces):
            subinterface["vlan"] = custom_variables.get("setup2_subinterface_" + str(index) + "_vlan", subinterface.get("vlan"))
            subinterface["description"] = custom_variables.get("setup2_subinterface_" + str(index) + "_description", subinterface.get("description"))
            subinterface["ip"] = custom_variables.get("setup2_subinterface_" + str(index) + "_ip", subinterface.get("ip"))
            subinterface["mask"] = custom_variables.get("setup2_subinterface_" + str(index) + "_mask", subinterface.get("mask"))

        for index, vlan in enumerate(vlans):
            vlan["id"] = custom_variables.get("setup2_vlan_" + str(index) + "_id", vlan.get("id"))
            vlan["name"] = custom_variables.get("setup2_vlan_" + str(index) + "_name", vlan.get("name"))

        switches["trunk_allowed_vlans"] = custom_variables.get(
            "switches_trunk_allowed_vlans",
            switches.get("trunk_allowed_vlans"),
        )

        for switch_name, switch_data in switches.items():
            if not isinstance(switch_data, dict):
                continue

            switch_data["hostname"] = custom_variables.get(switch_name + "_hostname", switch_data.get("hostname"))
            switch_data["management_ip"] = custom_variables.get(switch_name + "_management_ip", switch_data.get("management_ip"))

            trunk_ports = switch_data.get("trunk_ports", [])

            for index, trunk_port in enumerate(trunk_ports):
                trunk_port["interface"] = custom_variables.get(switch_name + "_trunk_" + str(index) + "_interface", trunk_port.get("interface"))
                trunk_port["description"] = custom_variables.get(switch_name + "_trunk_" + str(index) + "_description", trunk_port.get("description"))

            etherchannel = switch_data.get("etherchannel")

            if isinstance(etherchannel, dict):
                etherchannel["port_channel"] = custom_variables.get(switch_name + "_etherchannel_port_channel", etherchannel.get("port_channel"))
                etherchannel["mode"] = custom_variables.get(switch_name + "_etherchannel_mode", etherchannel.get("mode"))

                member_ports = etherchannel.get("member_ports", [])

                for index, member_port in enumerate(member_ports):
                    member_port["interface"] = custom_variables.get(switch_name + "_etherchannel_" + str(index) + "_interface", member_port.get("interface"))
                    member_port["description"] = custom_variables.get(switch_name + "_etherchannel_" + str(index) + "_description", member_port.get("description"))

            access_ports = switch_data.get("access_ports", [])

            for index, access_port in enumerate(access_ports):
                access_port["interface"] = custom_variables.get(switch_name + "_access_" + str(index) + "_interface", access_port.get("interface"))
                access_port["description"] = custom_variables.get(switch_name + "_access_" + str(index) + "_description", access_port.get("description"))
                access_port["vlan"] = custom_variables.get(switch_name + "_access_" + str(index) + "_vlan", access_port.get("vlan"))

    return runtime_data


def update_setup_info_file(setup_id, custom_variables):
    """
    Slaat aangepaste setupwaarden op in info.yml.

    Deze functie wordt pas gebruikt nadat de formulierwaarden gevalideerd zijn.
    Zo vermijden we dat foute IP's, VLANs of interfaces in info.yml terechtkomen.
    """

    setup_info = get_setup_info(setup_id)

    if setup_info == None:
        return {
            "status": "failed",
            "output": "Geen geldige setup gevonden voor setup_id " + str(setup_id),
        }

    info_pad = os.path.join(setup_info["pad"], "info.yml")

    try:
        nieuwe_info = build_runtime_variables(setup_info, custom_variables)

        with open(info_pad, "w", encoding="utf-8") as info_file:
            yaml.safe_dump(
                nieuwe_info,
                info_file,
                sort_keys=False,
                allow_unicode=True,
                default_flow_style=False,
            )

    except Exception as fout:
        return {
            "status": "failed",
            "output": "info.yml kon niet bijgewerkt worden: " + str(fout),
        }

    return {
        "status": "success",
        "output": "info.yml is bijgewerkt.",
    }


def maak_runtime_inventory(setup_info, runtime_variables, run_reference=None):
    """
    Maakt een tijdelijke inventory voor 1 configuratierun.

    Waarom?
    - de management-IP's staan in info.yml;
    - inventory.ini blijft een basisbestand;
    - Ansible moet verbinden met de IP's die nu in info.yml staan.
    """

    originele_inventory = setup_info["inventory"]
    runtime_inventory_map = os.path.join(BASE_DIR, "data", "runtime_inventories")
    os.makedirs(runtime_inventory_map, exist_ok=True)

    if run_reference:
        inventory_naam = run_reference + "-inventory.ini"
    else:
        inventory_naam = "setup" + str(setup_info["id"]) + "-runtime-inventory.ini"

    runtime_inventory_pad = os.path.join(runtime_inventory_map, inventory_naam)

    variables = runtime_variables.get("variables", {})
    management_ips = {}

    router = variables.get("router", {})

    if router.get("management_ip"):
        management_ips["r1"] = str(router.get("management_ip"))

    switch = variables.get("switch", {})

    if switch.get("management_ip"):
        management_ips["sw1"] = str(switch.get("management_ip"))

    switches = variables.get("switches", {})

    for switch_name, switch_data in switches.items():
        if isinstance(switch_data, dict) and switch_data.get("management_ip"):
            management_ips[switch_name] = str(switch_data.get("management_ip"))

    with open(originele_inventory, "r", encoding="utf-8") as inventory_file:
        inventory_regels = inventory_file.readlines()

    nieuwe_regels = []

    for regel in inventory_regels:
        nieuwe_regel = regel
        regel_zonder_spaties = regel.strip()

        for toestelnaam, management_ip in management_ips.items():
            if regel_zonder_spaties.startswith(toestelnaam + " ") and "ansible_host=" in regel_zonder_spaties:
                delen = regel_zonder_spaties.split()
                nieuwe_delen = []

                for deel in delen:
                    if deel.startswith("ansible_host="):
                        nieuwe_delen.append("ansible_host=" + management_ip)
                    else:
                        nieuwe_delen.append(deel)

                nieuwe_regel = " ".join(nieuwe_delen) + "\n"

        nieuwe_regels.append(nieuwe_regel)

    with open(runtime_inventory_pad, "w", encoding="utf-8") as inventory_file:
        inventory_file.writelines(nieuwe_regels)

    return runtime_inventory_pad


def run_playbook(playbook_pad, inventory_pad, logged_user=None, run_reference=None):
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

    if run_reference:
        # Deze referentie koppelt de Ansible-run aan de juiste backupmap.
        command.append("-e")
        command.append("run_reference=" + run_reference)

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
