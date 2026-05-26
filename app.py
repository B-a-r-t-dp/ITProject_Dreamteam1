from flask import Flask, render_template, request, redirect, session

from modules.database_tools import (
    init_database,
    verify_user,
    get_network_setups,
    save_deployment_log,
    get_last_deployment_log,
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

    return render_template(
        "dashboard.html",
        user=user,
        network_setups=network_setups,
        last_log=last_log,
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

    result = run_setup(
        setup_id,
        logged_user=session["username"],
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
