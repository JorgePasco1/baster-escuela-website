""" Routes related to trainers """

from flask import render_template, request, jsonify
from flask_login import login_required

from app.admin import admin_blueprint
from app.admin.crud_factory import update_one, delete_one, add_one
from app.common.database import get_items
from app.common.constants import PUBLIC_DATABASE


@admin_blueprint.route('/entrenadores')
@login_required
def admin_trainers_screen():
    """ Screen for trainers' administration """
    entrenadores = get_items("entrenadores", PUBLIC_DATABASE)

    return render_template('admin_personas.html', personas=entrenadores, type="entrenadores")


@admin_blueprint.route('/entrenadores/<_id>', methods=['GET', 'POST', 'DELETE'])
@login_required
def admin_trainer_screen(_id):
    """ Screen for single trainer administration """

    _type = 'entrenadores'
    if request.method == 'POST':
        updated = update_one(PUBLIC_DATABASE, _type, request, _id)
        if not updated:
            return jsonify({'message': 'Something went wrong'}), 500
        return '', 200

    if request.method == 'DELETE':
        deleted = delete_one(PUBLIC_DATABASE, _type, _id)

        if not deleted:
            return jsonify({'message': 'Something went wrong'}), 500

        return jsonify({"redirect_to": f"/{_type}"}), 200

    try:
        entrenador = next(iter(get_items(_type, PUBLIC_DATABASE,
                                         filters=[{'field': 'id', 'values': [_id]}])))
    except Exception:
        return f"Entrenador con id {_id} no encontrado, <a href='/atletas'>regresar</a>"

    return render_template('admin_persona.html', persona=entrenador, type=_type)


@admin_blueprint.route('/entrenadores/nuevo', methods=['GET', 'POST'])
@login_required
def admin_new_trainer_screen():
    """ Screen to add new trainer """
    _type = 'entrenadores'
    if request.method == 'POST':
        added = add_one(PUBLIC_DATABASE, _type, request)
        if not added:
            return jsonify({'message': 'Something went wrong'}), 500
        return '', 200

    return render_template('admin_persona.html', type=_type)
