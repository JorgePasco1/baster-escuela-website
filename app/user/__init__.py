from flask import Blueprint, render_template, request, jsonify

from ..helpers import dict_factory, write_blob_to_file, get_items, format_logros

user_blueprint = Blueprint('user', __name__, template_folder='templates', static_folder='static', static_url_path='/app/user/static/')


@user_blueprint.route('/')
def home():
    return render_template("index.html")


@user_blueprint.route('/about')
def about():
    name = 'about'
    directiva = get_items("miembros_directiva")
    entrenadores = get_items("entrenadores")
    hitos = get_items("hitos")

    return render_template(f"{name}.html", active=f"{name}", hitos=hitos,
                           directiva=directiva, entrenadores=entrenadores)


@user_blueprint.route('/atletas')
def atletas():
    name = 'atletas'
    atletas = get_items("atletas")
    logros = format_logros(get_items("logros", group_by="alumno_id"))

    return render_template(f"{name}.html", active=name, atletas=atletas, logros=logros)


@user_blueprint.route('/abierto')
def abierto():
    name = 'abierto'
    return render_template(f"{name}.html", active=name)


@user_blueprint.route('/productos')
def productos():
    name = 'productos'
    return render_template(f"{name}.html", active=name)


@user_blueprint.route('/api/v1/logros')
def send_logros():
    player_id = request.args.get('player_id')

    if not player_id:
        return jsonify({"message": "missing player id"}), 400

    filters = [{"field": "alumno_id", "values": [player_id]}]
    logros = get_items("logros", filters=filters)
    return jsonify({"message": "success", "items": logros}), 200
