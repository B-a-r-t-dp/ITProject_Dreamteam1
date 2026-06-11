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
import copy                     # Wordt gebruikt om de setupdata veilig te kopieren.
import yaml                     # Wordt gebruikt om info.yml te lezen.
import ipaddress                # Wordt gebruikt om IP-adressen te valideren.

###############################################################################
#                              Path variabelen                                #
###############################################################################

# We bouwen de paden op vanaf de projectmap.
# Zo werkt dit bestand ook als de projectmap bij iemand anders anders noemt.

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANSIBLE_DIR = os.path.join(BASE_DIR, "ansible")
PLAYBOOK_DIR = os.path.join(ANSIBLE_DIR, "playbooks")


###############################################################################
#                         Functies validatie setupwaarden                      #
###############################################################################

"""
- Deze functie controleert de waarden die de gebruiker in het dashboard invult.
"""
def validate_custom_variables(setup_id, custom_variables):  # custom_variables zijn de frontend variabelen.

    fouten = []

    def controleer_op_lege_velden(veldnaam, label):     
        variabele = custom_variables.get(veldnaam, "").strip()                                           # .get() voorkomt dat de applicatie crasht als een formulierwaarde ontbreekt.

        if variabele == "":
            fouten.append(label + " mag niet leeg zijn.")

        return variabele

    def controleer_ip(veldnaam, label):
        variabele = controleer_op_lege_velden(veldnaam, label)

        if variabele == "":
            return

        try:
            ipaddress.ip_address(variabele)
        except ValueError:
            fouten.append(label + " moet een geldig IP-adres zijn.")

    def controleer_vlan(veldnaam, label):
        variabele = controleer_op_lege_velden(veldnaam, label)

        if variabele == "":
            return

        if not variabele.isdigit():
            fouten.append(label + " moet een getal zijn.")
            return

        vlan_id = int(variabele)

        if vlan_id < 1 or vlan_id > 4094:
            fouten.append(label + " moet tussen 1 en 4094 liggen.")

    def controleer_vlan_lijst(veldnaam, label):                                                             # Sommige velden bevatten meerdere VLANs in 1 tekstveld, Bijvoorbeeld: 10,20,30
        variabele = controleer_op_lege_velden(veldnaam, label)

        if variabele == "":
            return

        vlan_variabelen = variabele.split(",")

        for vlan in vlan_variabelen:
            vlan = vlan.strip()                                                                             # Spaties rond elk VLAN-nummer verwijderen.

            if not vlan.isdigit():
                fouten.append(label + " mag alleen VLAN-nummers bevatten, gescheiden door komma's.")
                return

            vlan_id = int(vlan)

            if vlan_id < 1 or vlan_id > 4094:
                fouten.append(label + " bevat een VLAN buiten bereik 1-4094.")
                return

    def controleer_interface(veldnaam, label):                                                              # Een interfacenaam zoals GigabitEthernet0/1 mag geen spaties bevatten.
        variabele = controleer_op_lege_velden(veldnaam, label)

        if variabele == "":
            return

        if " " in variabele:
            fouten.append(label + " mag geen spaties bevatten.")

    def controleer_getal(veldnaam, label, minimum, maximum):                                                # Deze functie gebruiken we voor velden die een getal met een minimum en maximum nodig hebben, Bijvoorbeeld OSPF process of port-channel nummer.
        variabele = controleer_op_lege_velden(veldnaam, label)

        if variabele == "":
            return

        if not variabele.isdigit():
            fouten.append(label + " moet een getal zijn.")
            return

        getal = int(variabele)

        if getal < minimum or getal > maximum:
            fouten.append(label + " moet tussen " + str(minimum) + " en " + str(maximum) + " liggen.")

    def valideer_technische_documentatie(custom_variables, fouten):
        """
        Controleert alle velden van de technische documentatie.
        Deze velden beginnen in het formulier altijd met technical_documentation_.
        """
        # gaat gewoon technische documentatie checken dat title en intro is ingevuld om te zorgen dat de documentatie leesbaar blijft.
        for veldnaam in sorted(custom_variables.keys()):                                                    # Doorloop alle variabelen op naam.
            is_technische_documentatie = veldnaam.startswith("technical_documentation_")

            if is_technische_documentatie:
                label = veldnaam.replace("_", " ")
                controleer_op_lege_velden(veldnaam, label)

    # We valideren per setup apart, omdat setup1 en setup2 andere formulierwaarden gebruiken.
    setup_id = str(setup_id)

    # Controleer ook de technische documentatievelden.
    valideer_technische_documentatie(custom_variables, fouten)

    if setup_id == "1":
        # Setup1 heeft 1 router, 1 switch en servercontainers.
        # Hieronder controleren we alleen de velden die in het formulier aanpasbaar zijn.
        controleer_op_lege_velden("router_hostname", "Router hostname") # (variabel die nagekeken wordt, tekst bij die variabel die gegeven wordt bij de foutmeldingen)
        controleer_ip("router_management_ip", "Router management-IP")
        controleer_interface("router_lab_interface", "Router labinterface")
        controleer_op_lege_velden("router_lab_description", "Router labinterface beschrijving")
        controleer_ip("router_lab_ip", "Router lab IP-adres")
        controleer_ip("router_lab_mask", "Router lab subnetmasker")
        controleer_getal("router_ospf_process", "OSPF process", 1, 65535)
        controleer_ip("router_ospf_router_id", "OSPF router-id")
        controleer_ip("router_ospf_network", "OSPF netwerk")
        controleer_ip("router_ospf_wildcard", "OSPF wildcard")
        controleer_getal("router_ospf_area", "OSPF area", 0, 4294967295)

        controleer_op_lege_velden("switch_hostname", "Switch hostname")
        controleer_ip("switch_management_ip", "Switch management-IP")
        controleer_interface("switch_access_port", "Switch accesspoort")
        controleer_op_lege_velden("switch_access_description", "Switch accesspoort beschrijving")
        controleer_vlan("switch_access_vlan", "Switch access VLAN")
        controleer_interface("switch_trunk_port", "Switch trunkpoort")
        controleer_op_lege_velden("switch_trunk_description", "Switch trunk beschrijving")
        controleer_vlan_lijst("switch_trunk_allowed_vlans", "Toegelaten VLANs op trunk")

        # gaat vlannummer uit variabel_id halen en controlleren of het nummer klopt.
        for veldnaam in sorted(custom_variables.keys()):
            if veldnaam.startswith("setup1_vlan_") and veldnaam.endswith("_id"):              # Zoek setup1 VLAN-velden die een VLAN-nummer bevatten.
                vlan_index = veldnaam.replace("setup1_vlan_", "").replace("_id", "")          # Haal de index uit de veldnaam, bijvoorbeeld 0 of 1.
                controleer_vlan(veldnaam, "VLAN " + vlan_index + " nummer")                   # Controleer of het VLAN-nummer geldig is.
            # gaat vlan naam uit variabel_id halen om te controlleren of die is ingevuld.
            if veldnaam.startswith("setup1_vlan_") and veldnaam.endswith("_name"):            # Zoek setup1 VLAN-velden die een VLAN-naam bevatten.
                vlan_index = veldnaam.replace("setup1_vlan_", "").replace("_name", "")        # Haal de index uit de veldnaam, bijvoorbeeld 0 of 1.
                controleer_op_lege_velden(veldnaam, "VLAN " + vlan_index + " naam")           # Controleer of de VLAN-naam ingevuld is.

    if setup_id == "2":
        # Setup2 is groter: 1 router en meerdere switches.
        # Daarom zijn er meer dynamische velden dan bij setup1.
        controleer_op_lege_velden("router_hostname", "Router hostname")
        controleer_ip("router_management_ip", "Router management-IP")
        controleer_interface("router_trunk_interface", "Router trunkinterface")
        controleer_op_lege_velden("router_trunk_description", "Router trunk beschrijving")

        # Setup2 heeft dynamische lijsten voor subinterfaces en VLANs.
        # Daarom zoeken we de velden op basis van hun naamstructuur.
        for veldnaam in sorted(custom_variables.keys()):
            if veldnaam.startswith("setup2_subinterface_") and veldnaam.endswith("_vlan"):       # Zoek VLAN-nummers van router-subinterfaces.
                controleer_vlan(veldnaam, veldnaam.replace("_", " "))

            if veldnaam.startswith("setup2_subinterface_") and veldnaam.endswith("_description"): # Zoek beschrijvingen van router-subinterfaces.
                controleer_op_lege_velden(veldnaam, veldnaam.replace("_", " "))

            if veldnaam.startswith("setup2_subinterface_") and veldnaam.endswith("_ip"):         # Zoek IP-adressen van router-subinterfaces.
                controleer_ip(veldnaam, veldnaam.replace("_", " "))

            if veldnaam.startswith("setup2_subinterface_") and veldnaam.endswith("_mask"):       # Zoek subnetmaskers van router-subinterfaces.
                controleer_ip(veldnaam, veldnaam.replace("_", " "))

            if veldnaam.startswith("setup2_vlan_") and veldnaam.endswith("_id"):                 # Zoek algemene VLAN-nummers van setup2.
                controleer_vlan(veldnaam, veldnaam.replace("_", " "))

            if veldnaam.startswith("setup2_vlan_") and veldnaam.endswith("_name"):               # Zoek algemene VLAN-namen van setup2.
                controleer_op_lege_velden(veldnaam, veldnaam.replace("_", " "))

        for switch_name in ["sw11", "sw12", "distsw", "classsw"]:                                # Setup2 heeft meerdere switches.
            controleer_op_lege_velden(switch_name + "_hostname", switch_name.upper() + " hostname")
            controleer_ip(switch_name + "_management_ip", switch_name.upper() + " management-IP")

        # Setup2 heeft meerdere switchvelden voor trunks, EtherChannel en accesspoorten.
        # Daarom zoeken we opnieuw op basis van de vaste naamstructuur van het formulier.
        for veldnaam in sorted(custom_variables.keys()):
            if veldnaam.startswith(("sw11_trunk_", "sw12_trunk_", "distsw_trunk_", "classsw_trunk_")):  # Zoek trunkvelden van alle switches.
                if veldnaam.endswith("_interface"):
                    controleer_interface(veldnaam, veldnaam.replace("_", " "))

                if veldnaam.endswith("_description"):
                    controleer_op_lege_velden(veldnaam, veldnaam.replace("_", " "))

            if veldnaam.startswith(("distsw_etherchannel_", "classsw_etherchannel_")):           # Zoek EtherChannel-velden van DISTSW en CLASSSW.
                if veldnaam.endswith("_port_channel"):
                    controleer_getal(veldnaam, veldnaam.replace("_", " "), 1, 64)

                if veldnaam.endswith("_mode"):                                                  # EtherChannel mode mag alleen active, passive of on zijn.
                    # Dit veld controleren we apart omdat alleen deze 3 waarden geldig zijn.
                    waarde = custom_variables.get(veldnaam, "").strip()

                    if waarde == "":
                        fouten.append(veldnaam.replace("_", " ") + " mag niet leeg zijn.")

                    if waarde not in ["active", "passive", "on"]:
                        fouten.append(veldnaam.replace("_", " ") + " moet active, passive of on zijn.")

                if veldnaam.endswith("_interface"):
                    controleer_interface(veldnaam, veldnaam.replace("_", " "))

                if veldnaam.endswith("_description"):
                    controleer_op_lege_velden(veldnaam, veldnaam.replace("_", " "))

            if veldnaam.startswith("classsw_access_"):                                          # Zoek accesspoortvelden van de classroomswitch.
                if veldnaam.endswith("_interface"):
                    controleer_interface(veldnaam, veldnaam.replace("_", " "))

                if veldnaam.endswith("_description"):
                    controleer_op_lege_velden(veldnaam, veldnaam.replace("_", " "))

                if veldnaam.endswith("_vlan"):
                    controleer_vlan(veldnaam, veldnaam.replace("_", " "))

        controleer_vlan_lijst("switches_trunk_allowed_vlans", "Toegelaten VLANs op trunks")

    return fouten

###############################################################################
#                         Functies info.yml verwerken                         #
###############################################################################

"""
- Deze functie zet formulierwaarden om naar een structuur die past bij `info.yml`.
"""
def build_runtime_variables(setup_info, custom_variables=None):

    info_pad = os.path.join(setup_info["pad"], "info.yml")                                                  # Pad naar info.yml van de gekozen setup.

    with open(info_pad, "r", encoding="utf-8") as info_file:
        info_data = yaml.safe_load(info_file)                                                               # Leest YAML om naar gewone Python-data.

    setup_data = copy.deepcopy(info_data)                                                                   # We maken bewust een kopie van info.yml, Zo kunnen we waarden aanpassen zonder de originele data per ongeluk te wijzigen.

    if not custom_variables:                                                                                # Als er geen formulierwaarden zijn, gebruiken we info.yml zoals die nu is.
        return setup_data

    # Als er frontendwaarden zijn, passen we die aan in de kopie van info.yml.
    # De originele info.yml wordt pas later overschreven als alles gevalideerd is.
    setup_id = str(setup_info["id"])
    variabelen = setup_data.get("variables", {})  # Alle technische setupwaarden staan onder variables en worden opgehaald om dan aangepast te worden indien nodig..

    if setup_id == "1":
        router = variabelen.get("router", {})    # Routerblok uit info.yml.
        switch = variabelen.get("switch", {})    # Switchblok uit info.yml.

        # Routerwaarden van setup1 bijwerken met de formulierwaarden.
        router["hostname"] = custom_variables.get("router_hostname", router.get("hostname"))                            # nieuwe waarde uit frontend bestaat? -> gebruik die geen nieuwe waarde? -> behoud oude waarde uit info.yml
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

        # Switchwaarden van setup1 bijwerken met de formulierwaarden.
        switch["hostname"] = custom_variables.get("switch_hostname", switch.get("hostname"))
        switch["management_ip"] = custom_variables.get("switch_management_ip", switch.get("management_ip"))
        switch["access_port"] = custom_variables.get("switch_access_port", switch.get("access_port"))
        switch["access_description"] = custom_variables.get("switch_access_description", switch.get("access_description"))
        switch["access_vlan"] = custom_variables.get("switch_access_vlan", switch.get("access_vlan"))
        switch["trunk_port"] = custom_variables.get("switch_trunk_port", switch.get("trunk_port"))
        switch["trunk_description"] = custom_variables.get("switch_trunk_description", switch.get("trunk_description"))
        switch["trunk_allowed_vlans"] = custom_variables.get("switch_trunk_allowed_vlans", switch.get("trunk_allowed_vlans"))

        vlans = switch.get("vlans", [])          # Lijst met VLANs van setup1.

        # VLANs worden via index verwerkt omdat het formulier dezelfde volgorde gebruikt.
        for index, vlan in enumerate(vlans):
            vlan["id"] = custom_variables.get("setup1_vlan_" + str(index) + "_id", vlan.get("id"))
            vlan["name"] = custom_variables.get("setup1_vlan_" + str(index) + "_name", vlan.get("name"))

    if setup_id == "2":
        router = variabelen.get("router", {})      # Routerblok uit info.yml.
        vlans = variabelen.get("vlans", [])        # Algemene VLAN-lijst van setup2.
        switches = variabelen.get("switches", {})  # Alle switches van setup2.

        # Routerwaarden van setup2 bijwerken met de formulierwaarden.
        router["hostname"] = custom_variables.get("router_hostname", router.get("hostname"))
        router["management_ip"] = custom_variables.get("router_management_ip", router.get("management_ip"))
        router["trunk_interface"] = custom_variables.get("router_trunk_interface", router.get("trunk_interface"))
        router["trunk_description"] = custom_variables.get("router_trunk_description", router.get("trunk_description"))

        subinterfaces = router.get("subinterfaces", [])  # Subinterfaces van de router-on-a-stick configuratie.

        # Subinterfaces worden via index verwerkt omdat het formulier dezelfde volgorde gebruikt. dus elke subinterface krijgt een indexnummer die dan gebruikt wordt om de variabelen aan te passen.
        for index, subinterface in enumerate(subinterfaces):
            subinterface["vlan"] = custom_variables.get("setup2_subinterface_" + str(index) + "_vlan", subinterface.get("vlan"))
            subinterface["description"] = custom_variables.get("setup2_subinterface_" + str(index) + "_description", subinterface.get("description"))
            subinterface["ip"] = custom_variables.get("setup2_subinterface_" + str(index) + "_ip", subinterface.get("ip"))
            subinterface["mask"] = custom_variables.get("setup2_subinterface_" + str(index) + "_mask", subinterface.get("mask"))

        # Algemene VLAN-lijst van setup2 bijwerken.
        for index, vlan in enumerate(vlans): # gaat een index maken van de hoeveelheid vlans; index = 0, index = 1 omdat er 2vlans zijn.
            vlan["id"] = custom_variables.get("setup2_vlan_" + str(index) + "_id", vlan.get("id"))
            vlan["name"] = custom_variables.get("setup2_vlan_" + str(index) + "_name", vlan.get("name"))

        switches["trunk_allowed_vlans"] = custom_variables.get(
            "switches_trunk_allowed_vlans",
            switches.get("trunk_allowed_vlans"),
        )

        for switch_naam, switch_data in switches.items():
            # .items() geeft telkens de naam van de switch en de data van die switch.
            # Bijvoorbeeld: sw11 en het bijhorende blok uit info.yml.
            if not isinstance(switch_data, dict):
                # trunk_allowed_vlans is tekst en geen switchblok.
                # Daarom slaan we die hier over.
                continue

            # Elke switch heeft eigen formulierwaarden.
            # De naam uit info.yml, bijvoorbeeld sw11, komt overeen met de veldnamen.
            switch_data["hostname"] = custom_variables.get(switch_naam + "_hostname", switch_data.get("hostname"))
            switch_data["management_ip"] = custom_variables.get(switch_naam + "_management_ip", switch_data.get("management_ip"))

            trunk_ports = switch_data.get("trunk_ports", [])  # Trunkpoorten van deze switch.

            for index, trunk_port in enumerate(trunk_ports):
                trunk_port["interface"] = custom_variables.get(switch_naam + "_trunk_" + str(index) + "_interface", trunk_port.get("interface"))
                trunk_port["description"] = custom_variables.get(switch_naam + "_trunk_" + str(index) + "_description", trunk_port.get("description"))

            etherchannel = switch_data.get("etherchannel")  # EtherChannel bestaat alleen op sommige switches.

            if isinstance(etherchannel, dict):
                # Alleen als etherchannel echt een blok met data is, werken we die waarden bij.
                etherchannel["port_channel"] = custom_variables.get(switch_naam + "_etherchannel_port_channel", etherchannel.get("port_channel"))
                etherchannel["mode"] = custom_variables.get(switch_naam + "_etherchannel_mode", etherchannel.get("mode"))

                member_ports = etherchannel.get("member_ports", [])  # Fysieke poorten die samen 1 EtherChannel vormen.

                for index, member_port in enumerate(member_ports):
                    member_port["interface"] = custom_variables.get(switch_naam + "_etherchannel_" + str(index) + "_interface", member_port.get("interface"))
                    member_port["description"] = custom_variables.get(switch_naam + "_etherchannel_" + str(index) + "_description", member_port.get("description"))

            access_ports = switch_data.get("access_ports", [])  # Accesspoorten voor toestellen aan de classroomkant.

            for index, access_port in enumerate(access_ports):
                access_port["interface"] = custom_variables.get(switch_naam + "_access_" + str(index) + "_interface", access_port.get("interface"))
                access_port["description"] = custom_variables.get(switch_naam + "_access_" + str(index) + "_description", access_port.get("description"))
                access_port["vlan"] = custom_variables.get(switch_naam + "_access_" + str(index) + "_vlan", access_port.get("vlan"))

    update_technical_documentation(setup_data, custom_variables)  # Ook de tekstuele documentatie in info.yml bijwerken.

    return setup_data



"""
- Deze functie zet formulierwaarden om naar een structuur die past bij `info.yml`.
"""
def update_technical_documentation(setup_data, custom_variables):
    """
    Werkt de technische documentatie in info.yml bij.

    De structuur blijft dezelfde:
    - titel;
    - intro;
    - vaste secties;
    - vaste regels per sectie.

    We passen dus alleen de tekst aan, niet het aantal blokken.
    """

    technische_documentatie = setup_data.get("technical_documentation")  # Blok met leesbare documentatie uit info.yml.

    if not isinstance(technische_documentatie, dict):
        # Als een setup geen technische documentatie heeft, stoppen we gewoon.
        return

    technische_documentatie["title"] = custom_variables.get(
        "technical_documentation_title",
        technische_documentatie.get("title"),
    )

    technische_documentatie["intro"] = custom_variables.get(
        "technical_documentation_intro",
        technische_documentatie.get("intro"),
    )

    secties = technische_documentatie.get("sections", [])  # Lijst met documentatieblokken.

    for sectie_index, sectie in enumerate(secties):
        # enumerate geeft zowel de positie als de inhoud.
        # Die positie gebruiken we om de juiste formuliernaam terug te vinden.
        if not isinstance(sectie, dict):
            continue

        sectie["title"] = custom_variables.get(
            "technical_documentation_section_" + str(sectie_index) + "_title",
            sectie.get("title"),
        )

        regels = sectie.get("items", [])  # Regels tekst binnen deze documentatiesectie.

        for regel_index, regel in enumerate(regels):
            veldnaam = "technical_documentation_section_" + str(sectie_index) + "_item_" + str(regel_index)
            regels[regel_index] = custom_variables.get(veldnaam, regel)



"""
- Deze functie past `info.yml` effectief aan.
"""
def update_setup_info_file(setup_id, custom_variables):

    setup_info = get_setup_info(setup_id)

    if setup_info == None:
        # Zonder geldige setupmap weten we niet welke info.yml aangepast moet worden.
        return {
            "status": "failed",
            "output": "Geen geldige setup gevonden voor setup_id " + str(setup_id),
        }

    info_pad = os.path.join(setup_info["pad"], "info.yml")  # Bestand dat effectief aangepast wordt.

    try:
        # Eerst bouwen we de nieuwe inhoud op in Python.
        # Daarna schrijven we die pas naar info.yml.
        nieuwe_info = build_runtime_variables(setup_info, custom_variables)

        with open(info_pad, "w", encoding="utf-8") as info_file:
            yaml.safe_dump(
                nieuwe_info,
                info_file,
                sort_keys=False,             # Volgorde van info.yml zoveel mogelijk behouden.
                allow_unicode=True,          # Nederlandse tekens normaal bewaren.
                default_flow_style=False,    # YAML netjes onder elkaar schrijven.
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

###############################################################################
#                  Functies setup en inventory voorbereiden                    #
###############################################################################

"""
- Deze functie zoekt de map van een setup.
"""
def get_setup_info(setup_id):
    """
    Zoekt welke setupmap en inventory bij een setup horen.
    setup_id 1 is gelinkt aan map setup1.
    setup_id 2 is gelinkt aan map setup2.
    """

    setup_map_naam = "setup" + str(setup_id)  # Bijvoorbeeld setup1 of setup2.

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

"""
- Deze functie bepaalt welke playbooks bij een setup horen.
"""
def get_playbooks_for_setup(setup_info):

    setup_pad = setup_info["pad"]  # Dit is de map waar de playbooks van deze setup staan.

    # Dit zijn de playbooks die we verwachten in elke setupmap.
    # In de MVP houden we dit bewust hardcoded.
    mogelijke_playbooks = [
        os.path.join(setup_pad, "router.yml"),
        os.path.join(setup_pad, "switch.yml"),
        os.path.join(setup_pad, "servers.yml"),
    ]

    bestaande_playbooks = []  # Hierin komen alleen playbooks die echt bestaan.

    for playbook_pad in mogelijke_playbooks:
        if os.path.exists(playbook_pad):
            bestaande_playbooks.append(playbook_pad)

    return bestaande_playbooks

###############################################################################
#                         Functies tijdelijke inventory                        #
###############################################################################

"""
- Deze functie maakt per run een tijdelijke inventory in `data/runtime_inventories`.
"""
def maak_runtime_inventory(setup_info, setup_data, run_reference=None):
    """
    Waarom?
    - de management-IP's staan in info.yml;
    - inventory.ini blijft een basisbestand;
    - Ansible moet verbinden met de IP's die nu in info.yml staan.
    """

    originele_inventory = setup_info["inventory"]  

    # plaats waar runtime_inventorys worden opgeslaan.
    runtime_inventory_map = os.path.join(BASE_DIR, "data", "runtime_inventories")
    os.makedirs(runtime_inventory_map, exist_ok=True) 

    # hier bepalen we de naam van de tijdelijke inventory
    if run_reference:
        inventory_naam = run_reference + "-inventory.ini"
    else:
        inventory_naam = "setup" + str(setup_info["id"]) + "-runtime-inventory.ini"

    runtime_inventory_pad = os.path.join(runtime_inventory_map, inventory_naam)  # Volledig pad naar tijdelijke inventory.

    # Hier halen we de technische variabelen uit info.yml.
    # Daarna maken we een lege dictionary waarin we per toestel het juiste management-IP verzamelen.
    variabelen = setup_data.get("variables", {}) 
    management_ips = {}

    # routerblok zoeken in info.yml
        router = variabelen.get("router", {})

    # Als de router een management-IP heeft, bewaren we dat IP onder de inventorynaam r1.
    if router.get("management_ip"):
        management_ips["r1"] = str(router.get("management_ip"))

    # Hier zoeken we het switchblok van setup 1.
    switch = variabelen.get("switch", {})

    if switch.get("management_ip"):
        management_ips["sw1"] = str(switch.get("management_ip"))

    switches = variabelen.get("switches", {})

    # Setup2 heeft meerdere switches, bijvoorbeeld sw11, sw12, distsw en classsw.
    for switch_naam, switch_data in switches.items():

        # Hier controleren we of het echt een switchblok is en of er een management-IP instaat. Als dat zo is, bewaren we dat IP onder de juiste switchnaam.
        if isinstance(switch_data, dict) and switch_data.get("management_ip"):
            management_ips[switch_naam] = str(switch_data.get("management_ip"))

    # Hier lezen we de gewone inventory regel per regel in.
    with open(originele_inventory, "r", encoding="utf-8") as inventory_file:
        inventory_regels = inventory_file.readlines()

    nieuwe_regels = []  # Hierin bouwen we de aangepaste inventory op.

    # We lezen de vaste inventory en vervangen enkel ansible_host.
    # Alle andere groepsinstellingen blijven gewoon hetzelfde.
    for regel in inventory_regels:
        nieuwe_regel = regel
        regel_zonder_spaties = regel.strip()  # Nodig om makkelijker te controleren waarmee de regel start.

        # Hier lopen we door alle toestellen waarvan we een management-IP hebben verzameld.
        for toestelnaam, management_ip in management_ips.items():
            # Bijvoorbeeld: r1 ansible_host=192.168.0.215
            if regel_zonder_spaties.startswith(toestelnaam + " ") and "ansible_host=" in regel_zonder_spaties:
                delen = regel_zonder_spaties.split()  # Regel opdelen in losse stukken.
                
                nieuwe_delen = []                     # Hier komt dezelfde regel terug, maar met nieuw IP.

                for deel in delen:
                    # Als het stukje het IP-adres bevat, vervangen we het door het management-IP uit info.yml.
                    if deel.startswith("ansible_host="):
                        nieuwe_delen.append("ansible_host=" + management_ip)
                    else:
                        nieuwe_delen.append(deel)

                nieuwe_regel = " ".join(nieuwe_delen) + "\n"

        nieuwe_regels.append(nieuwe_regel)

    # Hier schrijven we de tijdelijke inventory effectief weg naar een bestand.
    with open(runtime_inventory_pad, "w", encoding="utf-8") as inventory_file:
        inventory_file.writelines(nieuwe_regels)  # Tijdelijke inventory wegschrijven.

    return runtime_inventory_pad

###############################################################################
#                         Functies opstart Ansible                            #
###############################################################################

"""
- Deze functie start de volledige Ansible-flow voor 1 setup.
"""
def run_setup(setup_id, logged_user=None, run_reference=None):
    ## VOORBEREIDINGSFASE ##
    setup_info = get_setup_info(setup_id)                                                           # Setupinfo opvragen volgens setup_id.

    if setup_info == None:
        # Als de setupmap of inventory ontbreekt, kunnen we niet starten.
        setup_info_status = {
            "status": "failed",
            "output": "Geen geldige setup gevonden voor setup_id " + str(setup_id),
        }
        return setup_info_status

    playbooks = get_playbooks_for_setup(setup_info)                                                 # Playbooks opvragen volgens de setupinfo.

    # variabelen voorbereiden
    setup_data = build_runtime_variables(setup_info)
    runtime_inventory = maak_runtime_inventory(setup_info, setup_data, run_reference)               # We lezen info.yml en maken daarna een tijdelijke inventory, Zo gebruikt Ansible altijd de management-IP's die op dat moment in info.yml staan.

    if not playbooks:                                                                               
        playbooks_status = {
            "status": "failed",
            "output": "Geen Ansible-playbooks gevonden voor setup_id " + str(setup_id),
        }
        return playbooks_status


    ## PLAYBOOKS WORDEN 1VOOR1 UITGEVOERD ##
    samenvatting_regels = []
    technische_output = []

    er_is_een_fout = False                                                                          # Deze variabele onthoudt of minstens 1 playbook gefaald is, Zo kan de volledige setup op failed gezet worden.

    for playbook_pad in playbooks:
        playbook_naam = os.path.basename(playbook_pad)                                              #  Haalt enkel de bestandsnaam uit het volledige pad.

        ansible_resultaat = run_playbook(
            playbook_pad,
            runtime_inventory,
            logged_user,
            run_reference,                                                                          # Wordt meegegeven vanuit de sqllitedb.
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
        "status": ansible_status,                               # True/False
        "output": ansible_output,                               # de output van de run.
    }

    return ansible_log

'''
- Deze functie start 1 Ansible-playbook.
'''
def run_playbook(playbook_pad, inventory_pad, logged_user=None, run_reference=None):

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

"""
- Deze functie combineert stdout en stderr van Ansible tot 1 tekstblok.
"""
def maak_technische_output(uitgevoerd_proces):
    """
    stdout = gewone Ansible-output
    stderr = waarschuwingen of foutdetails
    """

    output_delen = []  # Hier verzamelen we stdout en stderr in 1 leesbare tekst.

    if uitgevoerd_proces.stdout:
        outelen.append("ANSIBLE OUTPUT")put_d
        output_delen.append("")
        output_delen.append(uitgevoerd_proces.stdout)

    if uitgevoerd_proces.stderr:
        output_delen.append("WAARSCHUWINGEN / FOUTDETAILS")
        output_delen.append("")
        output_delen.append(uitgevoerd_proces.stderr)

    output = "\n".join(output_delen).strip()  # Alle delen samenvoegen en zet de tekst onder elkaar..

    if output == "":
        output = "Ansible gaf geen output terug."

    return output



"""
- Deze functie maakt de volledige tekst die in SQLite opgeslagen wordt.
"""
def maak_volledige_output(samenvatting_regels, technische_output):

    volledige_output = []  # Eerst samenvatting, daarna technische output.

    volledige_output.append("SAMENVATTING CONFIGURATIE")
    volledige_output.append("")
    volledige_output.extend(samenvatting_regels)
    volledige_output.append("")
    volledige_output.append("TECHNISCHE OUTPUT")
    volledige_output.append("")
    volledige_output.extend(technische_output)

    return "\n\n".join(volledige_output)


"""
- Deze functie probeert technische Ansible-fouten om te zetten naar mensentaal.
"""
def explain_ansible_error(output):

    output_lower = output.lower()  # Alles naar kleine letters zetten zodat zoeken makkelijker wordt.

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

