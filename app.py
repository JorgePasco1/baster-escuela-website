import os

from flask import Flask, render_template, request, jsonify
from helpers import dict_factory, write_blob_to_file, get_items, format_logros

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
HOST = os.environ.get('HOST') or "localhost:5000"
app.config["SERVER_NAME"] = HOST


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/about')
def about():
    name = 'about'
    directiva = get_items("miembros_directiva")
    entrenadores = get_items("entrenadores")
    hitos = get_items("hitos")

    return render_template(f"{name}.html", active=f"{name}", hitos=hitos,
                           directiva=directiva, entrenadores=entrenadores)


@app.route('/atletas')
def atletas():
    name = 'atletas'
    atletas = get_items("atletas")
    logros = format_logros(get_items("logros", group_by="alumno_id"))

    return render_template(f"{name}.html", active=f"{name}", atletas=atletas, logros=logros)


@app.route('/abierto')
def abierto():
    name = 'abierto'
    return render_template(f"{name}.html", active=f"{name}")


@app.route('/productos')
def productos():
    name = 'productos'
    return render_template(f"{name}.html", active=f"{name}")


@app.route('/api/v1/logros')
def send_logros():
    player_id = request.args.get('player_id')

    if not player_id:
        return jsonify({"message": "missing player id"}), 400

    filters = [{"field": "alumno_id", "values": [player_id]}]
    logros = get_items("logros", filters=filters)
    return jsonify({"message": "success", "items": logros}), 200


@app.route('/', subdomain='admin')
def admin_home():
    return 'Admin page'
