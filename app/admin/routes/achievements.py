""" Routes related to players' achievements """

from flask import render_template, request, jsonify
from flask_login import login_required

from app.admin import admin_blueprint
from app.admin.crud_factory import update_one, delete_one, add_one
from app.common.database import get_items
from app.common.constants import PUBLIC_DATABASE


@admin_blueprint.route('/logros-atletas', methods=['GET', 'POST'])
@login_required
def admin_logros_screen():
    """ Screen for players' achievements administration and route for new achievement submision"""

    if request.method == 'POST':
        add_one(PUBLIC_DATABASE, 'logros', request)

    logros = get_items("logros", PUBLIC_DATABASE)
    atletas = get_items("atletas", PUBLIC_DATABASE, fields=[
                        'id', 'nombre', 'apellido'])
    options = {
        "atleta": atletas,
        "tipo": {element.get('tipo') for element in logros if element.get('tipo')},
        "nivel_torneo": {element.get('nivel_torneo') for element in logros if element.get(
            'nivel_torneo')},
        "puesto": {element.get('puesto') for element in logros if element.get('puesto')},
        "categoria": {element.get('categoria') for element in logros if element.get('categoria')}
    }

    return render_template('admin_logros.html', options=options)
