""" Routes related to board of directors """

from flask import render_template, request, jsonify
from flask_login import login_required

from app.admin import admin_blueprint
from app.admin.crud_factory import update_one, delete_one, add_one
from app.common.database import get_items
from app.common.constants import PUBLIC_DATABASE
from app.common.helpers import month_text_to_number


@admin_blueprint.route('/hitos')
@login_required
def admin_hitos_screen():
    """ Screen for milestones administration """
    hitos = get_items("hitos", PUBLIC_DATABASE)

    return render_template('admin_hitos.html', hitos=hitos)


@admin_blueprint.route('/hitos/<_id>', methods=['GET', 'POST', 'DELETE'])
@login_required
def admin_hito_screen(_id):
    """ Screen for single milestone administration """

    _type = 'hitos'
    if request.method == 'POST':
        updated = update_one(PUBLIC_DATABASE, _type, request, _id)
        if not updated:
            return jsonify({'message': 'Something went wrong'}), 500

    if request.method == 'DELETE':
        deleted = delete_one(PUBLIC_DATABASE, _type, _id)

        if not deleted:
            return jsonify({'message': 'Something went wrong'}), 500

        return jsonify({"redirect_to": "/hitos"}), 200

    try:
        hito = next(iter(get_items(_type, PUBLIC_DATABASE,
                                         filters=[{'field': 'id', 'values': [_id]}])))
        hito['mes'] = month_text_to_number(hito['mes'])
    except Exception:
        return f"Hito con id {_id} no encontrado, <a href='/hitos'>regresar</a>"

    return render_template('admin_hito.html', hito=hito)


@admin_blueprint.route('/hitos/nuevo', methods=['GET', 'POST'])
@login_required
def admin_new_hito_screen():
    """ Screen to add new milestone """
    _type = 'hitos'
    if request.method == 'POST':
        added = add_one(PUBLIC_DATABASE, _type, request)
        if not added:
            return jsonify({'message': 'Something went wrong'}), 500

    return render_template('admin_hito.html', type=_type)
