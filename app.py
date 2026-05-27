import ipaddress
from flask import Flask, render_template, request, redirect, session

# from modules.database_tools import (
#     init_database,
#     verify_user,
#     get_network_setups,
#     save_deployment_log,
#     get_last_deployment_log,
# )

from modules.database_tools import (
    init_database,
    verify_user,
    get_network_setups,
    save_deployment_log,
    get_last_deployment_log,
    get_deployment_logs_for_user,
    get_backup_files,
)

from modules.ansible_tools import run_setup


app = Flask(__name__)
app.secret_key = "supersecretkey"


init_database()


@app.route("/", methods=["GET", "POST"])
def login():
    # Als de gebruiker al aangemeld is en opnieuw naar / gaat,
    # sturen we hem meteen naar het dashboard.
    # Zo komt een ingelogde gebruiker niet terug op de loginpagina.
    if request.method == "GET" and "user_id" in session:
        return redirect("/dashboard")

    error = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = verify_user(username, password)

        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]
            return redirect("/dashboard")

        error = "Ongeldige login"

    return render_template("login.html", error=error)


# @app.route("/dashboard")
# def dashboard():
#     if "user_id" not in session:
#         return redirect("/")

#     user = {
#         "id": session["user_id"],
#         "username": session["username"],
#         "role": session["role"],
#     }

#     network_setups = get_network_setups()
#     last_log = get_last_deployment_log(session["user_id"])

#     return render_template(
#         "dashboard.html",
#         user=user,
#         network_setups=network_setups,
#         last_log=last_log,
#     )

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")

    user = {
        "id": session["user_id"],
        "username": session["username"],
        "role": session["role"],
    }

    network_setups = get_network_setups()
    last_log = get_last_deployment_log(session["user_id"])
    deployment_logs = get_deployment_logs_for_user(session["user_id"], limit=10)
    backup_files = get_backup_files()

    return render_template(
        "dashboard.html",
        user=user,
        network_setups=network_setups,
        last_log=last_log,
        deployment_logs=deployment_logs,
        backup_files=backup_files,
    )
def validate_custom_variables(setup_id, custom_variables):
    """
    Controleert eenvoudige formulierwaarden voordat Ansible gestart wordt.

    We houden de controles bewust simpel:
    - hostnames mogen niet leeg zijn;
    - VLANs moeten getallen zijn tussen 1 en 4094;
    - IP-adressen moeten geldig zijn;
    - trunk VLAN-lijsten mogen niet leeg zijn.
    """

    errors = []

    def check_required(field_name, label):
        value = custom_variables.get(field_name, "").strip()
        if value == "":
            errors.append(label + " mag niet leeg zijn.")
        return value

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

    def check_ip(field_name, label):
        value = custom_variables.get(field_name, "").strip()

        if value == "":
            errors.append(label + " mag niet leeg zijn.")
            return

        try:
            ipaddress.ip_address(value)
        except ValueError:
            errors.append(label + " moet een geldig IP-adres zijn.")

    setup_id = str(setup_id)

    if setup_id == "1":
        check_required("router_hostname", "Router hostname")
        check_required("switch_hostname", "Switch hostname")
        check_required("router_lab_description", "Router LAN-beschrijving")
        check_required("switch_access_description", "Switch accesspoort beschrijving")
        check_required("switch_trunk_description", "Switch trunk beschrijving")
        check_required("switch_vlan_10_name", "VLAN 10 naam")
        check_required("switch_vlan_20_name", "VLAN 20 naam")

        check_ip("router_lab_ip", "Router lab IP-adres")
        check_required("router_lab_mask", "Router lab subnetmasker")
        check_ip("router_ospf_router_id", "OSPF router-id")

        check_vlan("switch_access_vlan", "Access VLAN")
        check_vlan_list("switch_trunk_allowed_vlans", "Toegelaten VLANs op trunk")

    if setup_id == "2":
        check_required("router_hostname", "Router hostname")
        check_required("router_trunk_description", "Router trunk beschrijving")
        check_required("vlan_10_name", "VLAN 10 naam")
        check_required("vlan_20_name", "VLAN 20 naam")
        check_required("sw11_hostname", "SW11 hostname")
        check_required("sw12_hostname", "SW12 hostname")
        check_required("distsw_hostname", "DISTSW hostname")
        check_required("classsw_hostname", "CLASSSW hostname")
        check_required("classsw_access_description", "Classroom accesspoort beschrijving")

        check_vlan("classsw_access_vlan", "Classroom access VLAN")
        check_vlan_list("switches_trunk_allowed_vlans", "Toegelaten VLANs op trunks")

    return errors

@app.route("/deploy", methods=["POST"])
def deploy():
    if "user_id" not in session:
        return redirect("/")

    setup_id = request.form.get("setup_id")

    try:
        setup_id = int(setup_id)
    except (TypeError, ValueError):
        return redirect("/dashboard")
    
    valid_setup_ids = [setup["id"] for setup in get_network_setups()]

    if setup_id not in valid_setup_ids:
        return redirect("/dashboard")

    custom_variables = request.form.to_dict()

    validation_errors = validate_custom_variables(setup_id, custom_variables)

    if validation_errors:
        result = {
            "status": "failed",
            "output": "VALIDATIEFOUTEN\n\n" + "\n".join(validation_errors),
        }

        save_deployment_log(
            user_id=session["user_id"],
            setup_id=setup_id,
            status=result["status"],
            output=result["output"],
        )

        return redirect("/dashboard")

    result = run_setup(
        setup_id,
        logged_user=session["username"],
        custom_variables=custom_variables,
    )

    save_deployment_log(
        user_id=session["user_id"],
        setup_id=setup_id,
        status=result["status"],
        output=result["output"],
    )

    return redirect("/dashboard")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
