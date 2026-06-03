
# =====================================================================
#
# WAT DOET DIT BESTAND?
# ---------------------------------------------------------------------
# Dit bestand bevat alle hulpfuncties om met de SQLite-database te werken.
# Je kan dit bestand zien als de database-laag van de applicatie.
#
# In plaats van SQL-query's rechtstreeks in app.py te schrijven, roept app.py
# functies uit dit bestand aan.
#
# Voorbeelden:
#
# - app.py wil een gebruiker controleren:
#       verify_user(username, password)
#
# - app.py wil alle netwerkopstellingen tonen:
#       get_network_setups()
#
# - app.py wil het resultaat van een configuratierun bewaren:
#       save_deployment_log(...)
#
# - app.py wil de laatste logs tonen:
#       get_deployment_logs_for_user(...)
#
# WAAROM IS DIT EEN GOEDE STRUCTUUR?
# ---------------------------------------------------------------------
# De Flask-routes blijven eenvoudiger en leesbaarder.
# app.py moet zich vooral bezighouden met webverkeer:
#
# - welke URL wordt opgevraagd;
# - is de gebruiker ingelogd;
# - welk template moet getoond worden;
# - welke functie moet aangeroepen worden.
#
# De database-details blijven hier in database_tools.py:
#
# - waar staat de database;
# - hoe maken we verbinding;
# - welke SQL-query wordt uitgevoerd;
# - hoe worden resultaten omgezet naar dictionaries voor Flask/templates.
#
# TAAKVERDELING BINNEN HET PROJECT
# ---------------------------------------------------------------------
# - Lina: Flask-routes, sessies en templates
# - Joost: database, tabellen, users, setups en logs
# - Bart: Ansible en Docker
#
# BELANGRIJK
# ---------------------------------------------------------------------
# Deze uitlegversie bevat veel commentaar om de code te kunnen verdedigen
# tijdens de evaluatie. De werking van de code blijft hetzelfde.
# Op het einde kunnen we hiervan een kortere definitieve versie maken.
# =====================================================================

# sqlite3 is de standaard Python-module om met SQLite-databases te werken.
# We moeten hiervoor geen aparte databaseserver installeren.
# SQLite bewaart alles in één bestand, in ons geval data/itproject.db.
import sqlite3

# pathlib.Path gebruiken we om bestandspaden op een nette, platformonafhankelijke
# manier op te bouwen. Dat is beter dan manueel strings aan elkaar plakken.
from pathlib import Path

# yaml gebruiken we om info.yml-bestanden te lezen.
# Deze bestanden bevatten extra beschrijvende info over een Ansible-setup.
import yaml

# Werkzeug levert functies om wachtwoorden veilig te hashen en te controleren.
# generate_password_hash() maakt een hash van een wachtwoord.
# check_password_hash() controleert later of een ingegeven wachtwoord klopt.
from werkzeug.security import generate_password_hash, check_password_hash

# datetime gebruiken we voor tijdstippen van deployment logs en backups.
from datetime import datetime

# ZoneInfo gebruiken we zodat tijdstippen in Belgische tijd kunnen worden gezet.
# Zonder dit zouden timestamps soms in UTC of systeem-/containertijd kunnen staan.
from zoneinfo import ZoneInfo


# =====================================================================
# CENTRALE PADEN
# =====================================================================
#
# Waarom zetten we deze paden bovenaan?
# ---------------------------------------------------------------------
# Zo hoeven we paden niet overal in de code opnieuw te typen.
# Als de projectstructuur later verandert, moeten we dit maar op één plaats
# aanpassen.
#
# Path(__file__) verwijst naar dit bestand zelf:
#
#     modules/database_tools.py
#
# .resolve() maakt daar een absoluut pad van.
# .parent gaat één map omhoog naar modules/.
# .parent.parent gaat nog één map omhoog naar de projectroot.
#
# BASE_DIR wordt dus de hoofdmap van het project.
# =====================================================================

BASE_DIR = Path(__file__).resolve().parent.parent

# Pad naar het SQLite-databasebestand.
# De database wordt bewust in de map data/ geplaatst.
DATABASE_PATH = BASE_DIR / "data" / "itproject.db"

# Pad naar het SQL-schema dat de tabellen aanmaakt.
SCHEMA_PATH = BASE_DIR / "database" / "schema.sql"

# Pad naar de Ansible-playbooks.
# Elke setup, zoals setup1 of setup2, heeft daar een eigen map.
PLAYBOOK_DIR = BASE_DIR / "ansible" / "playbooks"


# =====================================================================
# FUNCTIE: get_connection()
# =====================================================================
def get_connection():
    """
    Maakt verbinding met de SQLite-database.

    Deze functie wordt door bijna alle andere databasefuncties gebruikt.
    Het is dus de centrale toegangspoort tot SQLite.

    Wat gebeurt hier stap voor stap?

    1. We zorgen dat de map data/ bestaat.
    2. We openen of maken het databasebestand data/itproject.db.
    3. We stellen row_factory in op sqlite3.Row.
    4. We zetten foreign key-controle aan.
    5. We geven de databaseverbinding terug.

    Waarom is deze functie nuttig?

    app.py en de andere functies moeten niet weten waar de database exact staat
    of welke instellingen nodig zijn. Ze vragen gewoon een verbinding via
    get_connection().
    """

    # DATABASE_PATH.parent is de map data/.
    # mkdir(exist_ok=True) maakt de map aan als ze nog niet bestaat.
    # Als de map al bestaat, geeft dit geen fout.
    DATABASE_PATH.parent.mkdir(exist_ok=True)

    # sqlite3.connect() opent de database.
    # Als data/itproject.db nog niet bestaat, maakt SQLite dit bestand aan.
    connection = sqlite3.connect(DATABASE_PATH)

    # row_factory = sqlite3.Row zorgt ervoor dat we kolommen kunnen opvragen
    # via hun naam, bijvoorbeeld row["username"], in plaats van enkel via indexen
    # zoals row[1]. Dat maakt de code veel leesbaarder.
    connection.row_factory = sqlite3.Row

    # SQLite controleert foreign keys niet altijd automatisch.
    # Daarom zetten we dit bewust aan per verbinding.
    # Zo kan deployment_logs.user_id enkel verwijzen naar een bestaande user.
    connection.execute("PRAGMA foreign_keys = ON")

    # De verbinding wordt teruggegeven aan de functie die ze nodig heeft.
    return connection


# =====================================================================
# FUNCTIE: init_database()
# =====================================================================
def init_database():
    """
    Initialiseert de database.

    Deze functie wordt typisch aangeroepen bij het opstarten van de Flask-app.
    Ze zorgt ervoor dat de database klaar is om te gebruiken.

    Concreet doet deze functie vier grote dingen:

    1. Ze opent een verbinding met SQLite.
    2. Ze leest database/schema.sql en voert dat schema uit.
    3. Ze voegt standaardgebruikers toe voor de MVP/testomgeving.
    4. Ze voegt standaard netwerkopstellingen toe voor het dashboard.

    Belangrijk:
    De SQL gebruikt CREATE TABLE IF NOT EXISTS en INSERT OR IGNORE.
    Daardoor kan init_database() meerdere keren uitgevoerd worden zonder dat
    de app telkens crasht op bestaande tabellen of dubbele records.
    """

    # Open een verbinding met de database.
    connection = get_connection()

    # Lees het volledige schema.sql-bestand in.
    # encoding="utf-8" zorgt dat speciale tekens correct gelezen worden.
    with open(SCHEMA_PATH, "r", encoding="utf-8") as schema_file:
        schema_sql = schema_file.read()

    # executescript() kan meerdere SQL-statements na elkaar uitvoeren.
    # Dat is nodig omdat schema.sql meerdere CREATE TABLE- en CREATE INDEX-
    # statements bevat.
    connection.executescript(schema_sql)

    # Deze try/except is bedoeld voor bestaande databases.
    #
    # Waarom is dit nodig?
    # -----------------------------------------------------------------
    # Als je schema.sql aanpast en een nieuwe kolom toevoegt, dan krijgen
    # bestaande databases die kolom niet automatisch zolang de tabel al bestaat.
    # CREATE TABLE IF NOT EXISTS maakt de tabel namelijk niet opnieuw aan.
    #
    # Daarom proberen we run_reference apart toe te voegen met ALTER TABLE.
    # Als de kolom al bestaat, geeft SQLite een OperationalError.
    # Die fout negeren we bewust, omdat dat betekent dat alles al in orde is.
    try:
        connection.execute("ALTER TABLE deployment_logs ADD COLUMN run_reference TEXT")
    except sqlite3.OperationalError:
        pass

    # We maken een hash van het testwachtwoord.
    #
    # Het echte wachtwoord is hier "docent123".
    # In de database bewaren we niet "docent123" zelf, maar een hash.
    # Dat is veiliger dan wachtwoorden in platte tekst bewaren.
    password_hash = generate_password_hash("docent123")

    # Voeg standaardgebruikers toe.
    #
    # executemany() voert dezelfde SQL-query meerdere keren uit,
    # telkens met andere waarden.
    #
    # INSERT OR IGNORE betekent:
    # - bestaat deze username nog niet, voeg hem toe;
    # - bestaat hij al, doe niets en geef geen fout.
    #
    # De vraagtekens (?) zijn placeholders.
    # De echte waarden worden apart meegegeven.
    # Dat is veiliger en properder dan waarden rechtstreeks in SQL-strings plakken.
    connection.executemany(
        """
        INSERT OR IGNORE INTO users (username, password_hash, role)
        VALUES (?, ?, ?)
        """,
        [
            ("docent", password_hash, "teacher 1"),
            ("docent2", password_hash, "teacher 2"),
        ],
    )

    # Lijst met standaard netwerkopstellingen voor de MVP.
    #
    # Elk tuple bevat:
    #
    #   (id, name, description, playbook_data)
    #
    # playbook_data verwijst naar de map onder ansible/playbooks/.
    # Bijvoorbeeld setup2 verwijst naar ansible/playbooks/setup2/.
    network_setups = [
        (
            1,
            "Basisopstelling",
            "1 router, 1 switch, HTTP, HTTPS en FTP",
            "setup1",
        ),
        (
            2,
            "Podopstelling Brussel",
            "1 pod met router, 2 pod-switches, distributieswitch en classroomswitch",
            "setup2",
        ),
    ]

    # Voeg de netwerkopstellingen toe als ze nog niet bestaan.
    #
    # INSERT OR IGNORE voorkomt dubbele records wanneer init_database()
    # meerdere keren wordt uitgevoerd.
    connection.executemany(
        """
        INSERT OR IGNORE INTO network_setups
        (id, name, description, playbook_data)
        VALUES (?, ?, ?, ?)
        """,
        network_setups,
    )

    # Werk bestaande netwerkopstellingen bij.
    #
    # Waarom doen we na INSERT OR IGNORE ook nog UPDATE?
    # -----------------------------------------------------------------
    # Stel dat setup2 al bestaat, maar de description later aangepast werd.
    # INSERT OR IGNORE zou dan niets wijzigen omdat het record al bestaat.
    # Met deze UPDATE zorgen we dat naam, beschrijving en playbook_data toch
    # actueel blijven.
    connection.executemany(
        """
        UPDATE network_setups
        SET name = ?, description = ?, playbook_data = ?
        WHERE id = ?
        """,
        [
            # Hier herschikken we de volgorde van het tuple.
            # Origineel is setup = (id, name, description, playbook_data).
            # Voor de UPDATE willen we (name, description, playbook_data, id).
            (setup[1], setup[2], setup[3], setup[0])
            for setup in network_setups
        ],
    )

    # commit() schrijft alle wijzigingen definitief weg naar de database.
    # Zonder commit kunnen INSERT/UPDATE-wijzigingen verloren gaan.
    connection.commit()

    # Sluit de verbinding netjes af.
    # Dit voorkomt dat databaseverbindingen onnodig open blijven.
    connection.close()


# =====================================================================
# FUNCTIE: verify_user(username, password)
# =====================================================================
def verify_user(username, password):
    """
    Controleert of een gebruiker mag aanmelden.

    Deze functie wordt gebruikt bij de login.

    Input:
    - username: de ingegeven gebruikersnaam;
    - password: het ingegeven wachtwoord.

    Werking:
    1. Controleer of username en password ingevuld zijn.
    2. Zoek de gebruiker op in de tabel users.
    3. Als de gebruiker niet bestaat: return None.
    4. Controleer het wachtwoord met check_password_hash().
    5. Als het wachtwoord fout is: return None.
    6. Als alles klopt: geef een dictionary terug met usergegevens.

    Return bij correcte login:
    {
        "id": 1,
        "username": "docent",
        "role": "teacher 1"
    }

    Return bij fout:
    None
    """

    # Als username of password leeg is, stoppen we meteen.
    # Dan heeft het geen zin om de database te raadplegen.
    if not username or not password:
        return None

    # Open databaseverbinding.
    connection = get_connection()

    # Zoek de gebruiker op basis van username.
    #
    # We selecteren ook password_hash, want die hebben we nodig om het
    # ingegeven wachtwoord te controleren.
    #
    # De placeholder (?) voorkomt dat gebruikers invoer rechtstreeks in de
    # SQL-query terechtkomt. Dat helpt tegen SQL-injectie.
    user = connection.execute(
        """
        SELECT id, username, password_hash, role
        FROM users
        WHERE username = ?
        """,
        (username,),
    ).fetchone()

    # De query is uitgevoerd, dus de verbinding mag dicht.
    connection.close()

    # fetchone() geeft None terug als er geen gebruiker gevonden werd.
    if user is None:
        return None

    # Controleer het ingegeven wachtwoord tegenover de hash uit de database.
    # We vergelijken dus niet met een gewoon tekstwachtwoord.
    if not check_password_hash(user["password_hash"], password):
        return None

    # Als alles correct is, geven we alleen de nodige userinformatie terug.
    # We geven de password_hash bewust niet terug aan app.py of templates.
    return {
        "id": user["id"],
        "username": user["username"],
        "role": user["role"],
    }


# =====================================================================
# FUNCTIE: get_network_setups()
# =====================================================================
def get_network_setups():
    """
    Haalt alle beschikbare netwerkopstellingen op.

    app.py gebruikt deze functie om het dashboard te vullen.

    Wat doet deze functie?
    1. Lees alle records uit de tabel network_setups.
    2. Sorteer ze op id zodat ze in vaste volgorde verschijnen.
    3. Lees per setup extra informatie uit info.yml.
    4. Zet alles om naar een lijst van dictionaries.

    Waarom dictionaries?
    Templates zoals dashboard.html kunnen makkelijker werken met duidelijke
    sleutels zoals setup.name, setup.description en setup.info.
    """

    connection = get_connection()

    # Haal alle netwerkopstellingen uit de database.
    # ORDER BY id zorgt voor een voorspelbare volgorde op het dashboard.
    rows = connection.execute(
        """
        SELECT id, name, description, playbook_data
        FROM network_setups
        ORDER BY id
        """
    ).fetchall()

    connection.close()

    # We bouwen een gewone Python-lijst op voor gebruik in app.py/templates.
    network_setups = []

    for row in rows:
        # playbook_data bevat bijvoorbeeld "setup1" of "setup2".
        # Daarmee zoeken we extra uitleg in ansible/playbooks/setupX/info.yml.
        setup_info = get_setup_info(row["playbook_data"])

        # Voeg één setup toe als dictionary.
        network_setups.append(
            {
                "id": row["id"],
                "name": row["name"],
                "description": row["description"],
                "playbook_data": row["playbook_data"],
                "info": setup_info,
            }
        )

    return network_setups


# =====================================================================
# FUNCTIE: get_setup_info(setup_folder)
# =====================================================================
def get_setup_info(setup_folder):
    """
    Leest extra informatie over een netwerkopstelling.

    setup_folder is meestal "setup1" of "setup2".

    De functie zoekt naar:

        ansible/playbooks/<setup_folder>/info.yml

    Voorbeeld:

        ansible/playbooks/setup2/info.yml

    Waarom gebruiken we info.yml?
    -----------------------------------------------------------------
    De playbooks zelf zijn technisch en voeren de configuratie uit.
    info.yml kan in mensentaal beschrijven wat de setup doet.
    Daardoor kan het dashboard extra uitleg tonen zonder dat die uitleg
    hardcoded in HTML of Python moet staan.
    """

    # Bouw het pad naar info.yml op.
    info_path = PLAYBOOK_DIR / setup_folder / "info.yml"

    # Als het info.yml-bestand niet bestaat, geven we None terug.
    # Zo crasht de app niet wanneer een setup nog geen info.yml heeft.
    if not info_path.exists():
        return None

    # Lees het YAML-bestand en zet het om naar Python-data.
    # yaml.safe_load() is veiliger dan yaml.load(), omdat het geen willekeurige
    # Python-objecten probeert te maken.
    with open(info_path, "r", encoding="utf-8") as info_file:
        return yaml.safe_load(info_file)


# =====================================================================
# OUDE VERSIE VAN save_deployment_log() - NIET ACTIEF
# =====================================================================
#
# Dit blok is uitgecommentarieerd en wordt dus niet uitgevoerd.
# Het toont waarschijnlijk een eerdere versie van de functie.
#
# Verschil met de huidige actieve versie:
# - de oude versie had geen run_reference;
# - de oude versie liet SQLite zelf de timestamp invullen;
# - de nieuwe versie bewaart bewust Belgische tijd;
# - de nieuwe versie koppelt logs aan backupmappen via run_reference.
#
# We laten dit voorlopig staan als historiek/vergelijking in de uitlegversie.
# In een definitieve propere codeversie kan dit eventueel verwijderd worden.
# =====================================================================

# def save_deployment_log(user_id, setup_id, status, output):
#     """
#     Slaat het resultaat van een Ansible-uitvoering op.

#     status moet overeenkomen met de koppelafspraken:
#     - success
#     - failed
#     """

#     if status not in ("success", "failed"):
#         raise ValueError("status moet 'success' of 'failed' zijn")

#     connection = get_connection()

#     connection.execute(
#     """
#     INSERT INTO deployment_logs (user_id, setup_id, status, output)
#     VALUES (?, ?, ?, ?)
#     """,
#     (user_id, setup_id, status, output),
# )

#     connection.commit()
#     connection.close()


# =====================================================================
# FUNCTIE: save_deployment_log(...)
# =====================================================================
def save_deployment_log(user_id, setup_id, status, output, run_reference=None):
    """
    Slaat het resultaat van een Ansible-uitvoering op.

    Deze functie wordt aangeroepen nadat een configuratie via Ansible
    uitgevoerd werd.

    Input:
    - user_id:
      De gebruiker die de configuratie gestart heeft.

    - setup_id:
      De netwerkopstelling die gekozen werd.

    - status:
      Het resultaat van de configuratie.
      Toegelaten waarden zijn "success" en "failed".

    - output:
      De tekstuele output van Ansible of van onze eigen samenvatting.

    - run_reference:
      Een unieke referentie voor deze configuratierun.
      Die wordt gebruikt om de juiste backupmap te koppelen aan deze log.

    Waarom Belgische tijd?
    -----------------------------------------------------------------
    In containers, Linux-systemen of servers kan de systeemklok soms op UTC
    staan. Door Europe/Brussels expliciet te gebruiken, is het tijdstip duidelijk
    voor ons tijdens de test en presentatie.
    """

    # Controleer dat status alleen success of failed mag zijn.
    # Dit komt overeen met de CHECK constraint in schema.sql.
    # Zo vangen we fouten al op in Python voordat ze in de database komen.
    if status not in ("success", "failed"):
        raise ValueError("status moet 'success' of 'failed' zijn")

    # Maak een timestamp in Belgische tijd.
    # strftime() zet het datetime-object om naar een leesbare tekstvorm.
    belgian_time = datetime.now(ZoneInfo("Europe/Brussels")).strftime("%Y-%m-%d %H:%M:%S")

    connection = get_connection()

    # Voeg één nieuwe logregel toe.
    #
    # Let op de volgorde:
    # De kolommen in INSERT moeten overeenkomen met de volgorde van de waarden
    # in de tuple onderaan.
    connection.execute(
        """
        INSERT INTO deployment_logs (user_id, setup_id, timestamp, status, output, run_reference)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (user_id, setup_id, belgian_time, status, output, run_reference),
    )

    # Schrijf de INSERT definitief weg.
    connection.commit()

    # Sluit de verbinding.
    connection.close()


# =====================================================================
# FUNCTIE: split_deployment_output(output)
# =====================================================================
def split_deployment_output(output):
    """
    Splitst de Ansible-output in twee delen:

    1. summary
       Een korte, leesbare samenvatting voor het dashboard.

    2. technical_output
       De meer technische output voor wie details nodig heeft.

    Waarom doen we dit?
    -----------------------------------------------------------------
    Ansible-output kan lang en technisch zijn.
    Voor een docent/gebruiker is het handiger om eerst een duidelijke
    samenvatting te zien, met eventueel daaronder technische details.

    ansible_tools.py zet bewust een marker in de output:

        TECHNISCHE OUTPUT

    Deze functie gebruikt die marker om de tekst op te splitsen.
    """

    marker = "TECHNISCHE OUTPUT"

    # Als output leeg is of de marker ontbreekt, kunnen we niet splitsen.
    # Dan zetten we alles in summary en laten we technical_output leeg.
    if not output or marker not in output:
        return {
            "summary": output,
            "technical_output": "",
        }

    # split(marker, 1) splitst maar één keer.
    # Daardoor blijft eventuele extra tekst met dezelfde woorden in het tweede
    # deel gewoon behouden.
    summary, technical_output = output.split(marker, 1)

    # Verwijder de titel uit de samenvatting zodat het dashboard properder toont.
    summary = summary.replace("SAMENVATTING CONFIGURATIE", "").strip()

    # strip() verwijdert overbodige spaties en lege regels aan begin/einde.
    technical_output = technical_output.strip()

    return {
        "summary": summary,
        "technical_output": technical_output,
    }


# =====================================================================
# FUNCTIE: get_last_deployment_log(user_id=None)
# =====================================================================
def get_last_deployment_log(user_id=None):
    """
    Geeft de laatste deployment log terug.

    Als user_id wordt meegegeven:
        Toon enkel de laatste log van die gebruiker.

    Als user_id None is:
        Toon de laatste log van alle gebruikers samen.

    Waarom JOINs?
    -----------------------------------------------------------------
    deployment_logs bevat vooral id's:
    - user_id
    - setup_id

    Voor het dashboard willen we niet enkel die nummers tonen.
    We willen ook de username en setup_name tonen.
    Daarom joinen we deployment_logs met users en network_setups.
    """

    connection = get_connection()

    if user_id:
        # Haal de laatste log op voor één specifieke gebruiker.
        row = connection.execute(
            """
            SELECT deployment_logs.id, user_id, setup_id, network_setups.name AS setup_name, timestamp, status, output, run_reference, users.username
            FROM deployment_logs
            JOIN users ON users.id = deployment_logs.user_id
            JOIN network_setups ON network_setups.id = deployment_logs.setup_id
            WHERE user_id = ?
            ORDER BY deployment_logs.id DESC
            LIMIT 1
            """,
            (user_id,),
        ).fetchone()

    else:
        # Haal de laatste log op, ongeacht gebruiker.
        row = connection.execute(
            """
            SELECT deployment_logs.id, user_id, setup_id, network_setups.name AS setup_name, timestamp, status, output, run_reference, users.username
            FROM deployment_logs
            JOIN users ON users.id = deployment_logs.user_id
            JOIN network_setups ON network_setups.id = deployment_logs.setup_id
            ORDER BY deployment_logs.id DESC
            LIMIT 1
            """
        ).fetchone()

    connection.close()

    # Als er nog geen logs bestaan, geven we None terug.
    # app.py of dashboard.html kan dan beslissen om niets of een melding te tonen.
    if row is None:
        return None

    # Splits de output in samenvatting en technische output.
    split_output = split_deployment_output(row["output"])

    # Bouw een dictionary voor app.py/templates.
    # We voegen ook backups toe door run_reference door te geven aan
    # get_backup_files_for_run().
    return {
        "id": row["id"],
        "user_id": row["user_id"],
        "username": row["username"],
        "setup_id": row["setup_id"],
        "setup_name": row["setup_name"],
        "timestamp": row["timestamp"],
        "status": row["status"],
        "output": row["output"],
        "run_reference": row["run_reference"],
        "summary": split_output["summary"],
        "technical_output": split_output["technical_output"],
        "backups": get_backup_files_for_run(row["run_reference"]),
    }


# =====================================================================
# FUNCTIE: get_deployment_logs_for_user(user_id=None, limit=10)
# =====================================================================
def get_deployment_logs_for_user(user_id=None, limit=10):
    """
    Geeft de laatste deployment logs terug.

    Deze functie lijkt op get_last_deployment_log(), maar geeft meerdere logs
    terug in plaats van één enkele log.

    Parameters:
    - user_id:
      Als dit ingevuld is, tonen we enkel logs van die gebruiker.
      Als dit None is, tonen we logs van alle gebruikers.

    - limit:
      Maximum aantal logs dat we willen tonen.
      Standaard is dit 10, zodat het dashboard niet meteen een enorme lijst toont.

    Return:
    Een lijst van dictionaries. Elke dictionary stelt één logregel voor.
    """

    connection = get_connection()

    if user_id:
        # Logs van één specifieke gebruiker.
        rows = connection.execute(
            """
            SELECT deployment_logs.id, user_id, setup_id, network_setups.name AS setup_name, timestamp, status, output, run_reference, users.username
            FROM deployment_logs
            JOIN users ON users.id = deployment_logs.user_id
            JOIN network_setups ON network_setups.id = deployment_logs.setup_id
            WHERE user_id = ?
            ORDER BY deployment_logs.id DESC
            LIMIT ?
            """,
            (user_id, limit),
        ).fetchall()

    else:
        # Logs van alle gebruikers.
        rows = connection.execute(
            """
            SELECT deployment_logs.id, user_id, setup_id, network_setups.name AS setup_name, timestamp, status, output, run_reference, users.username
            FROM deployment_logs
            JOIN users ON users.id = deployment_logs.user_id
            JOIN network_setups ON network_setups.id = deployment_logs.setup_id
            ORDER BY deployment_logs.id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    connection.close()

    logs = []

    for row in rows:
        # Splits elke logoutput in een samenvatting en technische output.
        split_output = split_deployment_output(row["output"])

        # Voeg één log toe aan de lijst.
        logs.append({
            "id": row["id"],
            "user_id": row["user_id"],
            "username": row["username"],
            "setup_id": row["setup_id"],
            "setup_name": row["setup_name"],
            "timestamp": row["timestamp"],
            "status": row["status"],
            "output": row["output"],
            "run_reference": row["run_reference"],
            "summary": split_output["summary"],
            "technical_output": split_output["technical_output"],
            "backups": get_backup_files_for_run(row["run_reference"]),
        })

    return logs


# =====================================================================
# FUNCTIE: get_backup_files_for_run(run_reference)
# =====================================================================
def get_backup_files_for_run(run_reference):
    """
    Geeft de backupbestanden terug voor één configuratierun.

    De backups staan in:

        backups/<run_reference>/

    Voorbeeld:

        backups/20260603_143012_setup2/

    Waarom gebruiken we run_reference?
    -----------------------------------------------------------------
    Eén configuratierun kan meerdere backups opleveren, bijvoorbeeld van
    verschillende routers of switches.

    Door alle bestanden onder backups/<run_reference>/ te plaatsen, kunnen we
    exact tonen welke backups bij welke deployment log horen.
    """

    # Als er geen run_reference is, kunnen we geen backupmap bepalen.
    # Dan geven we gewoon een lege lijst terug.
    if not run_reference:
        return []

    # Basismap waarin alle backups staan.
    backup_dir = BASE_DIR / "backups"

    # Map voor deze specifieke run.
    run_backup_dir = backup_dir / run_reference

    # Als de backupmap niet bestaat, zijn er geen backups voor deze run.
    if not run_backup_dir.exists():
        return []

    backup_files = []

    # Overloop alle items in de backupmap.
    for file_path in run_backup_dir.iterdir():
        # We willen enkel echte bestanden tonen.
        # .gitkeep is een leeg bestand dat soms gebruikt wordt om een lege map
        # toch in Git te kunnen bewaren. Dat tonen we niet als echte backup.
        if file_path.is_file() and file_path.name != ".gitkeep":
            backup_files.append({
                # Bestandsnaam zoals die op het dashboard getoond kan worden.
                "name": file_path.name,

                # Relatief pad ten opzichte van de projectroot.
                # Dat is netter dan een volledig absoluut pad van de computer.
                "path": str(file_path.relative_to(BASE_DIR)),

                # Laatste wijzigingstijd van het bestand in Belgische tijd.
                "modified": datetime.fromtimestamp(
                    file_path.stat().st_mtime,
                    ZoneInfo("Europe/Brussels")
                ).strftime("%Y-%m-%d %H:%M:%S"),
            })

    # Sorteer de bestanden op wijzigingsdatum, nieuwste eerst.
    backup_files.sort(key=lambda item: item["modified"], reverse=True)

    return backup_files
