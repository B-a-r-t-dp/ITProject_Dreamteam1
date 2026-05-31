from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from flask import Flask, render_template, request, redirect, session, send_from_directory


from modules.database_tools import (
    init_database,
    verify_user,
    get_network_setups,
    save_deployment_log,
    get_last_deployment_log,
    get_deployment_logs_for_user,
)

from modules.ansible_tools import run_setup, validate_custom_variables


app = Flask(__name__)
app.secret_key = "supersecretkey"


init_database()


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

    return render_template(
        "dashboard.html",
        user=user,
        network_setups=network_setups,
        last_log=last_log,
        deployment_logs=deployment_logs,
    )


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
    run_reference = maak_run_referentie(setup_id, session["username"])

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
            run_reference=run_reference,
        )

        return redirect("/dashboard")

    result = run_setup(
        setup_id,
        logged_user=session["username"],
        custom_variables=custom_variables,
        run_reference=run_reference,
    )

    save_deployment_log(
        user_id=session["user_id"],
        setup_id=setup_id,
        status=result["status"],
        output=result["output"],
        run_reference=run_reference,
    )

    return redirect("/dashboard")


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

    backup_root = Path(app.root_path) / "backups"
    backup_map = backup_root / run_reference

    # Simpele beveiliging: alleen bestanden uit de backups-map toelaten.
    backup_root = backup_root.resolve()
    backup_map = backup_map.resolve()

    if backup_root not in backup_map.parents:
        return redirect("/dashboard")

    return send_from_directory(backup_map, filename, as_attachment=True)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
