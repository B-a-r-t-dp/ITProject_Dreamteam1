from flask import Flask, render_template


# Eigenaar: Lina
# Doel:
# - Flask-applicatie opstarten
# - routes maken voor login en dashboard
# - later login/logout en startknop voor Ansible koppelen
# Koppelt later met:
# - Joost: SQLite-functies uit modules/database_tools.py
# - Bart: Ansible-functies uit modules/ansible_tools.py
#
# Vaste koppelafspraken staan in:
# docs/koppelafspraken.md

app = Flask(__name__)


@app.route("/")
def login():
    """
    Loginpagina.

    Verantwoordelijke: Lina

    Later gebruikt deze route:
    - verify_user(username, password) uit modules/database_tools.py

    Verwacht gedrag later:
    - GET toont loginformulier;
    - POST controleert username/password;
    - bij succes naar dashboard;
    - bij fout foutmelding tonen.
    """
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    """
    Dashboardpagina.

    Verantwoordelijke: Lina

    Later gebruikt deze route:
    - get_network_setups() uit modules/database_tools.py
    - get_last_deployment_log() uit modules/database_tools.py

    Verwacht gedrag later:
    - alleen toegankelijk na login;
    - toont naam van docent;
    - toont beschikbare netwerkopstellingen;
    - toont laatste status/output.
    """
    return render_template("dashboard.html")


@app.route("/deploy", methods=["POST"])
def deploy():
    """
    Start configuratie voor een gekozen netwerkopstelling.

    Verantwoordelijke: Lina voor de route, Bart voor run_setup, Joost voor logging.

    Later gebruikt deze route:
    - run_setup(setup_id) uit modules/ansible_tools.py
    - save_deployment_log(user_id, setup_id, status, output) uit modules/database_tools.py

    Verwacht gedrag later:
    - setup_id lezen uit het formulier;
    - Ansible-flow starten;
    - status/output opslaan in SQLite;
    - terugkeren naar dashboard.
    """
    return "TODO: deploy-route nog uitwerken."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
