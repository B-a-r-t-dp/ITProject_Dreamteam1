from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import check_password_hash
import subprocess
import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"


# ------------------------
# Database helper
# ------------------------
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row  # zodat je dict-style kan gebruiken
    return conn


# ------------------------
# LOGIN
# ------------------------
@app.route("/", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()

        user = db.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]

            return redirect("/dashboard")
        else:
            error = "Ongeldige login"

    return render_template("login.html", error=error)


# ------------------------
# DASHBOARD
# ------------------------
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")

    db = get_db()

    # Alle setups
    setups = db.execute(
        "SELECT * FROM network_setups"
    ).fetchall()

    # Laatste deployment
    last_log = db.execute("""
        SELECT * FROM deployment_logs
        WHERE user_id = ?
        ORDER BY timestamp DESC
        LIMIT 1
    """, (session["user_id"],)).fetchone()

    user = {
        "username": session["username"]
    }

    return render_template(
        "dashboard.html",
        user=user,
        network_setups=setups,
        last_log=last_log
    )


# ------------------------
# DEPLOY (Ansible trigger)
# ------------------------
@app.route("/deploy", methods=["POST"])
def deploy():
    if "user_id" not in session:
        return redirect("/")

    setup_id = request.form["setup_id"]

    db = get_db()

    setup = db.execute(
        "SELECT * FROM network_setups WHERE id = ?",
        (setup_id,)
    ).fetchone()

    playbook = setup["playbook_data"]

    try:
        result = subprocess.run(
            ["ansible-playbook", playbook],
            capture_output=True,
            text=True
        )

        status = "SUCCESS" if result.returncode == 0 else "FAILED"
        output = result.stdout

    except Exception as e:
        status = "ERROR"
        output = str(e)

    # Log opslaan
    db.execute("""
        INSERT INTO deployment_logs
        (user_id, setup_id, timestamp, status, output)
        VALUES (?, ?, ?, ?, ?)
    """, (
        session["user_id"],
        setup_id,
        datetime.datetime.now(),
        status,
        output
    ))

    db.commit()

    return redirect("/dashboard")


# ------------------------
# LOGOUT
# ------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ------------------------
# START APP
# ------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)