# Module voor werken met datum en tijd.
# Wordt gebruikt voor het genereren van tijdstempels
# bij configuratieruns en logging.
from datetime import datetime

# Module voor het veilig werken met bestanden en mappen.
# Wordt gebruikt bij het beheren en downloaden van backups.
from pathlib import Path

# Module voor tijdzones.
# Wordt gebruikt om tijdstempels weer te geven volgens
# de Belgische tijdzone (Europe/Brussels).
from zoneinfo import ZoneInfo

# Flask                -> Aanmaken van de Flask-webapplicatie.
# render_template      -> Laden en weergeven van HTML-pagina's.
# request              -> Uitlezen van gegevens uit formulieren en URL-aanvragen.
# redirect             -> Doorsturen van gebruikers naar een andere pagina.
# session              -> Opslaan van gebruikersgegevens tijdens een sessie.
# send_from_directory  -> Aanbieden van bestanden als download.
from flask import Flask, render_template, request, redirect, session, send_from_directory


from modules.database_tools import (
    init_database,
    verify_user,
    get_network_setups,
    save_deployment_log,
    get_last_deployment_log,
    get_deployment_logs_for_user,
)

from modules.ansible_tools import (
    run_setup,
    validate_custom_variables,
    update_setup_info_file,
)

# Initialisatie van de Flask-applicatie.
# Flask gebruikt __name__ om de locatie van templates,
# statische bestanden en configuraties correct te bepalen.
app = Flask(__name__)

# Geheime sleutel voor sessiebeheer -> session[...] die opgeslagen in cookie
# Wordt gebruikt om sessiegegevens veilig te ondertekenen
# zodat gebruikers deze niet kunnen manipuleren.
app.secret_key = "supersecretkey"

# Initialiseren van de SQLite-database.
# Bij het opstarten van de applicatie worden de nodige
# tabellen aangemaakt indien deze nog niet bestaan.
init_database()

# --------------------------------------------------
# Functie: maak_run_referentie()
#
# Doel:
# Genereert een unieke referentie voor iedere
# configuratierun.
#
# Gebruik:
# - Opslaan van deployment logs in SQLite
# - Aanmaken van unieke backupmappen
#
# Parameters:
# setup_id  -> ID van de gekozen opstelling
# username  -> aangemelde gebruiker
#
# Return:
# String met unieke runreferentie
# --------------------------------------------------

def maak_run_referentie(setup_id, username):
    """
    Maakt een unieke naam voor 1 configuratierun.

    Die naam gebruiken we:
    - in SQLite bij de deployment log;
    - als mapnaam in backups/.
    """

    tijdstip = datetime.now(ZoneInfo("Europe/Brussels")).strftime("%Y%m%d-%H%M%S")

    run_referentie = "run-" + tijdstip + "-" + username + "-setup" + str(setup_id)

    return run_referentie



# --------------------------------------------------
# Route: /
#
# Doel:
# Loginpagina van de applicatie.
#
# Werking:
# - Toont loginformulier (GET)
# - Controleert gebruikersnaam en wachtwoord (POST)
# - Maakt een sessie aan bij succesvolle login
# - Stuurt gebruiker door naar dashboard
#
# Template:
# login.html
#
# Sessies:
# user_id
# username
# role
# --------------------------------------------------
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

        # Controle van gebruikersnaam en wachtwoord.
        # De functie verify_user() vergelijkt de ingevoerde
        # gegevens met de gebruikers in de database.
        user = verify_user(username, password)

        if user:
            # Bij succesvolle login worden de gebruikersgegevens
            # opgeslagen in de sessie zodat de gebruiker niet
            # opnieuw moet aanmelden bij elke pagina.
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]
            return redirect("/dashboard")

        error = "Ongeldige login"

    return render_template("login.html", error=error)




# --------------------------------------------------
# Route: /dashboard
#
# Doel:
# Hoofdscherm van de applicatie tonen.
#
# Werking:
# - Controleert of gebruiker ingelogd is
# - Haalt netwerkopstellingen op
# - Haalt laatste configuratierun op
# - Toont configuratiegeschiedenis
# - Ondersteunt filtering op:
#   * setup
#   * status
#   * gebruiker
#
# Template:
# dashboard.html
# --------------------------------------------------
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")

    user = {
        "id": session["user_id"],
        "username": session["username"],
        "role": session["role"],
    }

    # Ophalen van alle beschikbare netwerkopstellingen.
    # Deze worden weergegeven als configuratiekaarten
    # op het dashboard.
    network_setups = get_network_setups()

    # Ophalen van de meest recente configuratierun
    # van de huidige gebruiker.
    last_log = get_last_deployment_log(session["user_id"])

    # Ophalen van de laatste configuratieruns.
    # Deze worden gebruikt voor de sectie
    # 'Configuratiegeschiedenis'.
    deployment_logs = get_deployment_logs_for_user(limit=50)

    setup_update_feedback = session.pop("setup_update_feedback", None)

    # Opbouwen van een unieke lijst gebruikers
    # zodat deze gebruikt kunnen worden als filter
    # in de configuratiegeschiedenis.
    history_users = []
    history_user_ids = []

    for log in deployment_logs:
        if log["user_id"] not in history_user_ids:
            history_user_ids.append(log["user_id"])
            history_users.append({
                "id": log["user_id"],
                "username": log["username"],
            })

    # Filter op gekozen netwerkopstelling.
    # Enkel logs van de geselecteerde setup blijven zichtbaar.
    history_setup_filter = request.args.get("history_setup", "all")

    # Filter op resultaat van de configuratie.
    # Mogelijke waarden:
    # - success
    # - failed
    history_status_filter = request.args.get("history_status", "all")

    # Filter op gebruiker zodat enkel de runs
    # van een bepaalde gebruiker worden getoond.
    history_user_filter = request.args.get("history_user", "all")

    if history_setup_filter != "all":
        try:
            history_setup_id = int(history_setup_filter)
        except (TypeError, ValueError):
            history_setup_id = None

        if history_setup_id:
            deployment_logs = [
                log for log in deployment_logs
                if log["setup_id"] == history_setup_id
            ]

    if history_status_filter in ("success", "failed"):
        deployment_logs = [
            log for log in deployment_logs
            if log["status"] == history_status_filter
        ]

    if history_user_filter != "all":
        try:
            history_user_id = int(history_user_filter)
        except (TypeError, ValueError):
            history_user_id = None

        if history_user_id:
            deployment_logs = [
                log for log in deployment_logs
                if log["user_id"] == history_user_id
            ]

    history_filters = {
        "setup": history_setup_filter,
        "status": history_status_filter,
        "user": history_user_filter,
    }

    return render_template(
        "dashboard.html",
        user=user,
        network_setups=network_setups,
        last_log=last_log,
        deployment_logs=deployment_logs,
        history_users=history_users,
        setup_update_feedback=setup_update_feedback,
        history_filters=history_filters,
    )




# --------------------------------------------------
# Route: /deploy
#
# Doel:
# Start een Ansible-configuratie.
#
# Werking:
# - Controleert sessie
# - Valideert setup-ID
# - Genereert runreferentie
# - Start gekozen netwerkopstelling
# - Slaat resultaat op in deployment_logs
#
# Methode:
# POST
#
# Resultaat:
# Gebruiker wordt teruggestuurd naar dashboard
# --------------------------------------------------
@app.route("/deploy", methods=["POST"])
def deploy():
    if "user_id" not in session:
        return redirect("/")

    setup_id = request.form.get("setup_id")

    try:
        setup_id = int(setup_id)
    except (TypeError, ValueError):
        return redirect("/dashboard")
    
    # Controleren of de gekozen setup bestaat.
    # Hierdoor kan een gebruiker geen ongeldige
    # setup-ID doorsturen via een aangepast formulier.
    valid_setup_ids = [setup["id"] for setup in get_network_setups()]

    if setup_id not in valid_setup_ids:
        return redirect("/dashboard")

    # Voor iedere configuratierun wordt een unieke
    # referentie aangemaakt. Deze referentie wordt
    # gebruikt voor logging en backupbestanden.
    run_reference = maak_run_referentie(setup_id, session["username"])

    # Start de gekozen Ansible-configuratie.
    # De functie voert de playbook uit en geeft
    # een resultaat terug (success of failed).
    result = run_setup(
        setup_id,
        logged_user=session["username"],
        run_reference=run_reference,
    )

    # Opslaan van het resultaat in SQLite.
    # Hierdoor blijft een historiek van alle
    # uitgevoerde configuraties beschikbaar.
    save_deployment_log(
        user_id=session["user_id"],
        setup_id=setup_id,
        status=result["status"],
        output=result["output"],
        run_reference=run_reference,
    )

    return redirect("/dashboard")




# --------------------------------------------------
# Route: /update-setup-variables
#
# Doel:
# Aanpasbare configuratiewaarden bewaren zonder
# Ansible uit te voeren.
#
# Werking:
# - Leest formuliergegevens uit dashboard
# - Valideert invoer
# - Schrijft gegevens weg naar info.yml
# - Geeft succes- of foutmelding terug
#
# Methode:
# POST
# --------------------------------------------------
@app.route("/update-setup-variables", methods=["POST"])
def update_setup_variables():
    """
    Past de waarden in info.yml aan zonder Ansible te starten.

    Eerst valideren we de formulierwaarden.
    Pas als alles klopt, schrijven we ze effectief weg naar info.yml.
    """

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

    # Alle formulierwaarden worden verzameld
    # zodat ze gevalideerd kunnen worden.
    custom_variables = request.form.to_dict()

    # Controle van de ingevoerde configuratiewaarden.
    # Bijvoorbeeld:
    # - verplichte velden ingevuld
    # - geldig IP-adres
    # - correcte hostnaam
    validation_errors = validate_custom_variables(setup_id, custom_variables)

    if validation_errors:
        session["setup_update_feedback"] = {
            "setup_id": setup_id,
            "status": "failed",
            "messages": validation_errors,
        }

        return redirect("/dashboard")


    # Indien alle waarden geldig zijn,
    # worden ze opgeslagen in info.yml.
    # Deze waarden kunnen later door
    # Ansible gebruikt worden.
    update_result = update_setup_info_file(setup_id, custom_variables)

    if update_result["status"] == "failed":
        session["setup_update_feedback"] = {
            "setup_id": setup_id,
            "status": "failed",
            "messages": [update_result["output"]],
        }

        return redirect("/dashboard")

    session["setup_update_feedback"] = {
        "setup_id": setup_id,
        "status": "success",
        "messages": ["De waarden zijn gevalideerd en opgeslagen in info.yml."],
    }

    return redirect("/dashboard")




# --------------------------------------------------
# Route: /backup/<run_reference>/<filename>
#
# Doel:
# Downloaden van running-config backups.
#
# Werking:
# - Controleert sessie
# - Controleert geldig pad
# - Levert bestand aan gebruiker
#
# Beveiliging:
# Enkel bestanden uit de backups-map
# worden toegelaten.
# --------------------------------------------------
@app.route("/backup/<run_reference>/<filename>")
def download_backup(run_reference, filename):
    """
    Downloadt een backupbestand dat bij 1 configuratierun hoort.

    We werken bewust met een run-map:
    backups/<run_reference>/<bestand>
    Daardoor moet de frontend niet gokken welke backup bij welke run hoort.
    """

    if "user_id" not in session:
        return redirect("/")

    # Locatie van alle configuratiebackups.
    # Iedere configuratierun krijgt een eigen map.
    backup_root = Path(app.root_path) / "backups"

    backup_map = backup_root / run_reference

    # Extra beveiliging tegen path traversal.
    # Hiermee voorkomen we dat een gebruiker
    # bestanden buiten de backupmap kan downloaden.
    backup_root = backup_root.resolve()
    backup_map = backup_map.resolve()

    if backup_root not in backup_map.parents:
        return redirect("/dashboard")

    # Download van het gevraagde backupbestand.
    # Het bestand wordt als bijlage aangeboden
    # zodat de browser een download start.
    return send_from_directory(backup_map, filename, as_attachment=True)




# --------------------------------------------------
# Route: /logout
#
# Doel:
# Afmelden van de gebruiker.
#
# Werking:
# - Verwijdert alle sessiegegevens
# - Stuurt gebruiker terug naar loginpagina
# --------------------------------------------------
@app.route("/logout")
def logout():

    # Verwijderen van alle actieve sessiegegevens.
    # Hierdoor wordt de gebruiker volledig afgemeld.
    session.clear()

    return redirect("/")


if __name__ == "__main__":

    # Start van de Flask-webserver.
    # host="0.0.0.0" maakt de applicatie bereikbaar
    # vanaf andere toestellen in hetzelfde netwerk.
    # debug=True toont foutmeldingen tijdens ontwikkeling.
    app.run(host="0.0.0.0", port=5000, debug=True)
