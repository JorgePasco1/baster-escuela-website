"""
Admin Blueprint
"""
import os
from werkzeug.utils import secure_filename

from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app.common.database import get_items, add_new_item_to_db, update_record_in_db
from app.common.file_system import check_allowed_file, save_file_to_multiple_directories

admin_blueprint = Blueprint('admin', __name__, template_folder='templates',
                            static_folder='static', static_url_path='/app/admin/static')


PUBLIC_DATABASE = './baster_escuela.db'
BASE_PUBLIC_STATIC_URL = 'app/user/static/'
BASE_ADMIN_STATIC_URL = 'app/admin/static/'


@admin_blueprint.route('/')
def admin_redirect():
    """ Redirect '/' route to /home """
    return redirect(url_for('.admin_index'))


@admin_blueprint.route('/home')
@login_required
def admin_index():
    """ Homepage for admins """
    return render_template('admin_home.html', user_name=current_user.name)


@admin_blueprint.route('/logros-alumnos', methods=['GET', 'POST'])
@login_required
def admin_logros_screen():
    """ Screen for players' achievements administration and route for new achievement submision"""

    if request.method == 'POST':
        add_new_item_to_db('logros', PUBLIC_DATABASE, request.form)

    logros = get_items("logros", PUBLIC_DATABASE)
    alumnos = get_items("atletas", PUBLIC_DATABASE, fields=[
                        'id', 'nombre', 'apellido'])
    options = {
        "alumno": alumnos,
        "tipo": {element.get('tipo') for element in logros if element.get('tipo')},
        "nivel_torneo": {element.get('nivel_torneo') for element in logros if element.get(
            'nivel_torneo')},
        "puesto": {element.get('puesto') for element in logros if element.get('puesto')},
        "categoria": {element.get('categoria') for element in logros if element.get('categoria')}
    }

    return render_template('admin_logros.html', options=options)


@admin_blueprint.route('/alumnos')
@login_required
def admin_players_screen():
    """ Screen for players' administration """
    alumnos = get_items("atletas", PUBLIC_DATABASE)

    return render_template('admin_alumnos.html', atletas=alumnos)


@admin_blueprint.route('/alumnos/<_id>', methods=['GET', 'POST'])
@login_required
def admin_athlete_screen(_id):
    """ Screen for players' administration """

    if request.method == 'POST':
        public_upload_folder = BASE_PUBLIC_STATIC_URL + (os.environ.get(
            'ALUMNOS_UPLOAD_FOLDER') or 'img/photos/')
        admin_upload_folder = BASE_ADMIN_STATIC_URL + (os.environ.get(
            'ALUMNOS_UPLOAD_FOLDER') or 'img/photos/')

        _file = request.files['file']
        alumno_info = dict(request.form)
        filename = None

        if _file and check_allowed_file(_file.filename):
            extension = _file.filename.rsplit('.', 1)[1].lower()
            filename = f"atleta-{_id}.{extension}"

            save_file_to_multiple_directories(
                _file, filename, [public_upload_folder, admin_upload_folder])

            alumno_info['foto'] = f"{public_upload_folder.split('static/')[1]}/{filename}"

        update_record_in_db('atletas', PUBLIC_DATABASE,
                            alumno_info, {'id': _id})

    try:
        alumno = next(iter(get_items("atletas", PUBLIC_DATABASE,
                                     filters=[{'field': 'id', 'values': [_id]}])))
    except:
        return f"Alumnno con id {_id} no encontrado, <a href='/alumnos'>regresar</a>"

    return render_template('admin_atleta.html', atleta=alumno)


@admin_blueprint.route('/alumnos/nuevo', methods=['GET', 'POST'])
@login_required
def admin_new_athlete_screen():
    """ Screen to add new player """
    if request.method == 'POST':
        inserted_row_id = add_new_item_to_db(
            'atletas', PUBLIC_DATABASE, request.form)

        public_upload_folder = BASE_PUBLIC_STATIC_URL + (os.environ.get(
            'ALUMNOS_UPLOAD_FOLDER') or 'img/photos/')
        admin_upload_folder = BASE_ADMIN_STATIC_URL + (os.environ.get(
            'ALUMNOS_UPLOAD_FOLDER') or 'img/photos/')

        _file = request.files['file']
        filename = None

        if _file and check_allowed_file(_file.filename):
            extension = _file.filename.rsplit('.', 1)[1].lower()
            filename = f"atleta-{inserted_row_id}.{extension}"

            save_file_to_multiple_directories(
                _file, filename, [public_upload_folder, admin_upload_folder])

            info = {
                "foto": f"{public_upload_folder.split('static/')[1]}/{filename}"}

            update_record_in_db('atletas', PUBLIC_DATABASE,
                                info, {'id': inserted_row_id})

    return render_template('admin_atleta.html')

# TODO: Elimianar alumno
