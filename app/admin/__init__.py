"""
Admin Blueprint
"""
import os
from werkzeug.utils import secure_filename

from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app.helpers import get_items, add_new_item_to_db, check_allowed_file, \
    save_file_to_multiple_directories

admin_blueprint = Blueprint('admin', __name__, template_folder='templates',
                            static_folder='static', static_url_path='/app/admin/static')


PUBLIC_DATABASE = './baster_escuela.db'


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
    alumnos = get_items("atletas", PUBLIC_DATABASE, create_img=True)

    return render_template('admin_alumnos.html', atletas=alumnos)


@admin_blueprint.route('/alumnos/<_id>', methods=['GET', 'POST'])
@login_required
def admin_athlete_screen(_id):
    """ Screen for players' administration """

    if request.method == 'POST':
        public_upload_folder = os.environ.get(
            'PUBLIC_ALUMNOS_UPLOAD_FOLDER') or 'app/user/static/img/photos/'
        admin_upload_folder = os.environ.get(
            'ADMIN_ALUMNOS_UPLOAD_FOLDER') or 'app/admin/static/img/photos/'

        _file = request.files['file']
        alumno_info = request.form

        filename = None
        if _file and check_allowed_file(_file.filename):
            nombre = alumno_info['nombre'].replace(' ', '-')
            apellido = f"{alumno_info['apellido'].replace(' ', '-')}"
            extension = _file.filename.rsplit('.', 1)[1].lower()
            filename = f"{_id}-{nombre}-{apellido}1.{extension}"

            save_file_to_multiple_directories(
                _file, filename, [public_upload_folder, admin_upload_folder])

    alumno = next(iter(get_items("atletas", PUBLIC_DATABASE,
                                 create_img=True, filters=[{'field': 'id', 'values': _id}])))

    return render_template('admin_atleta.html', atleta=alumno)
