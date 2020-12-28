""" Routes related to board of directors """

from flask import render_template, request, jsonify
from flask_login import login_required

from app.admin import admin_blueprint
from app.admin.crud_factory import update_one, delete_one, add_one
from app.common.database import get_items
from app.common.constants import PUBLIC_DATABASE


@admin_blueprint.route('/directiva')
@login_required
def admin_directiva_miembros_screen():
    """ Screen for directiva members administration """
    miembros = get_items("miembros_directiva", PUBLIC_DATABASE)

    return render_template('admin_personas.html', personas=miembros, type="directiva")


@admin_blueprint.route('/directiva/<_id>', methods=['GET', 'POST', 'DELETE'])
@login_required
def admin_directiva_miembro_screen(_id):
    """ Screen for single directiva member administration """

    _type = 'miembros_directiva'
    if request.method == 'POST':
        updated = update_one(PUBLIC_DATABASE, _type, request, _id)
        if not updated:
            return jsonify({'message': 'Something went wrong'}), 500

    if request.method == 'DELETE':
        deleted = delete_one(PUBLIC_DATABASE, _type, _id)

        if not deleted:
            return jsonify({'message': 'Something went wrong'}), 500

        return jsonify({"redirect_to": "/directiva"}), 200

    try:
        miembro_directiva = next(iter(get_items(_type, PUBLIC_DATABASE,
                                         filters=[{'field': 'id', 'values': [_id]}])))
    except Exception:
        return f"Miembro de directiva con id {_id} no encontrado, <a href='/directiva'>regresar</a>"

    return render_template('admin_persona.html', persona=miembro_directiva, type='directiva')


@admin_blueprint.route('/directiva/nuevo', methods=['GET', 'POST'])
@login_required
def admin_new_directiva_miembro_screen():
    """ Screen to add new trainer """
    _type = 'miembros_directiva'
    if request.method == 'POST':
        added = add_one(PUBLIC_DATABASE, _type, request)
        if not added:
            return jsonify({'message': 'Something went wrong'}), 500
        return '', 200

    return render_template('admin_persona.html', type='directiva')
