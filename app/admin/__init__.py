"""
Admin Blueprint
"""

from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app.helpers import get_items, add_new_item_to_db

admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


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
def amin_players_screen():
    """ Screen for players' achievements administration and route for new achievement submision"""

    if request.method == 'POST':
        add_new_item_to_db('logros', PUBLIC_DATABASE, request.form)

    logros = get_items("logros", PUBLIC_DATABASE)
    alumnos = get_items("atletas", PUBLIC_DATABASE, fields=[
                        'id', 'nombre', 'apellido'])
    options = {
        "alumno": alumnos,
        "tipo": {element.get('tipo') for element in logros if element.get('tipo')},
        "nivel_torneo": {element.get('nivel_torneo') for element in logros if element.get('nivel_torneo')},
        "puesto": {element.get('puesto') for element in logros if element.get('puesto')},
        "categoria": {element.get('categoria') for element in logros if element.get('categoria')}
    }

    return render_template('admin_logros.html', options=options)
