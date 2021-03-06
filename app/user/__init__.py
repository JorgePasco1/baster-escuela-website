""" Entrypoint of public user Blueprint """

from flask import Blueprint, render_template, request, jsonify, url_for

from app.common.database import get_items
from app.common.helpers import format_logros
from app.common.constants import BASE_PUBLIC_STATIC_URL
from app.common.file_system import get_all_file_names_in_a_folder

user_blueprint = Blueprint('user', __name__, template_folder='templates',
                           static_folder='static', static_url_path='/app/user/static/')


PUBLIC_DATABASE = './baster_escuela.db'


@user_blueprint.route('/')
def home():
    """ Public Home """
    return render_template("index.html")


@user_blueprint.route('/about')
def about():
    """ Renders About Page """
    name = 'about'
    directiva = get_items("miembros_directiva", PUBLIC_DATABASE)
    entrenadores = get_items("entrenadores", PUBLIC_DATABASE)
    hitos = get_items("hitos", PUBLIC_DATABASE, order_by=[
                      ['año', 'ASC'], ['mes', 'ASC']])

    return render_template(f"{name}.html", active=f"{name}", hitos=hitos,
                           directiva=directiva, entrenadores=entrenadores)


@user_blueprint.route('/atletas')
def atletas():
    """ Renders page about the athletes """
    name = 'atletas'
    _atletas = get_items("atletas", PUBLIC_DATABASE)
    logros = format_logros(
        get_items("logros", PUBLIC_DATABASE, group_by="alumno_id"))

    return render_template(f"{name}.html", active=name, atletas=_atletas, logros=logros)


@user_blueprint.route('/abierto')
def abierto():
    """ Renders page about the school's tournament """
    name = 'abierto'
    filenames = get_all_file_names_in_a_folder(
        f'{BASE_PUBLIC_STATIC_URL}/img/photos/abierto')
    auspiciadores = get_all_file_names_in_a_folder(
        f'{BASE_PUBLIC_STATIC_URL}/img/photos/auspiciadores-abierto-2019')
    return render_template(f"{name}.html", active=name, filenames=filenames, auspiciadores=auspiciadores)


@user_blueprint.route('/productos')
def productos():
    """ Renders product listing page """
    name = 'productos'
    return render_template(f"{name}.html", active=name)


@user_blueprint.route('/api/v1/logros')
def send_logros():
    """ Returns json with the achievements by athlete """
    player_id = request.args.get('player_id')

    if not player_id:
        return jsonify({"message": "missing player id"}), 400

    filters = [{"field": "atleta_id", "values": [player_id]}]
    logros = get_items("logros", PUBLIC_DATABASE, filters=filters)
    return jsonify({"message": "success", "items": logros}), 200
