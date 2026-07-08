import csv
import os
import re
import threading
from datetime import datetime, timezone

from flask import Flask, render_template, request, send_file, abort

app = Flask(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
CSV_PATH = os.path.join(DATA_DIR, "reponses.csv")
FIELDNAMES = [
    "horodatage",
    "nom_groupe",
    "iban",
    "swift",
    "nom_banque",
    "lieu_banque",
    "nom_titulaire",
    "lieu_titulaire",
]

ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "")
_csv_lock = threading.Lock()


def iban_valide(iban: str) -> bool:
    iban = iban.replace(" ", "").upper()
    if not re.match(r"^[A-Z]{2}\d{2}[A-Z0-9]{11,30}$", iban):
        return False
    rearranged = iban[4:] + iban[:4]
    numeric = "".join(str(int(ch, 36)) for ch in rearranged)
    return int(numeric) % 97 == 1


def swift_valide(swift: str) -> bool:
    swift = swift.replace(" ", "").upper()
    return bool(re.match(r"^[A-Z]{6}[A-Z0-9]{2}([A-Z0-9]{3})?$", swift))


def valider_champs(form):
    erreurs = {}
    valeurs = {champ: form.get(champ, "").strip() for champ in FIELDNAMES[1:]}

    for champ in ("nom_groupe", "nom_banque", "lieu_banque", "nom_titulaire", "lieu_titulaire"):
        if not valeurs[champ]:
            erreurs[champ] = "Ce champ est obligatoire."

    if not valeurs["iban"]:
        erreurs["iban"] = "Ce champ est obligatoire."
    elif not iban_valide(valeurs["iban"]):
        erreurs["iban"] = "Format IBAN invalide."

    if valeurs["swift"] and not swift_valide(valeurs["swift"]):
        erreurs["swift"] = "Format SWIFT/BIC invalide (8 ou 11 caractères)."

    return valeurs, erreurs


def enregistrer(valeurs):
    os.makedirs(DATA_DIR, exist_ok=True)
    ligne = {
        "horodatage": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "nom_groupe": valeurs["nom_groupe"],
        "iban": valeurs["iban"].replace(" ", "").upper(),
        "swift": valeurs["swift"].replace(" ", "").upper(),
        "nom_banque": valeurs["nom_banque"],
        "lieu_banque": valeurs["lieu_banque"],
        "nom_titulaire": valeurs["nom_titulaire"],
        "lieu_titulaire": valeurs["lieu_titulaire"],
    }
    with _csv_lock:
        fichier_existe = os.path.isfile(CSV_PATH)
        with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            if not fichier_existe:
                writer.writeheader()
            writer.writerow(ligne)


@app.route("/", methods=["GET", "POST"])
def formulaire():
    if request.method == "POST":
        valeurs, erreurs = valider_champs(request.form)
        if not erreurs:
            enregistrer(valeurs)
            return render_template("index.html", succes=True, valeurs={})
        return render_template("index.html", succes=False, valeurs=valeurs, erreurs=erreurs)
    return render_template("index.html", succes=False, valeurs={}, erreurs={})


@app.route("/export")
def export():
    token = request.args.get("token", "")
    if not ADMIN_TOKEN or token != ADMIN_TOKEN:
        abort(403)
    if not os.path.isfile(CSV_PATH):
        abort(404)
    return send_file(CSV_PATH, as_attachment=True, download_name="reponses.csv")


if __name__ == "__main__":
    app.run(debug=True)
