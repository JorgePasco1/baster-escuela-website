""" Routes related to players' achievements """

from flask import render_template, request, jsonify
from flask_login import login_required

from app.admin import admin_blueprint
from app.admin.crud_factory import update_one, delete_one, add_one
from app.common.database import get_items
from app.common.helpers import format_logros
from app.common.constants import PUBLIC_DATABASE


@admin_blueprint.route('/logros-atletas', methods=['GET', 'POST'])
@login_required
def admin_add_logros_screen():
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

    return render_template('admin_add_logros.html', options=options)


@admin_blueprint.route('/atletas/<athlete_id>/logros')
def athletes_achievements(athlete_id):
    """ Get all achievements for an athlete """
    _type = 'logros'

    atleta = next(iter(get_items('atletas', PUBLIC_DATABASE, filters=[
                       {'field': 'id', 'values': [athlete_id]}])))
    achievements = format_logros(get_items(_type, PUBLIC_DATABASE, filters=[
        {'field': 'alumno_id', 'values': [athlete_id]}]))

    return render_template('admin_atleta_logros.html', atleta=atleta, logros=achievements)


@admin_blueprint.route('/atletas/<athlete_id>/logros/<logro_id>', methods=['GET', 'POST', 'DELETE'])
def atleta_achievement_screen(athlete_id, logro_id):
    """ Screen for player's achievement administration """
    _type = 'logros'

    if request.method == 'POST':
        updated = update_one(PUBLIC_DATABASE, _type, request, logro_id)
        if not updated:
            return jsonify({'message': 'Something went wrong'}), 500

    if request.method == 'DELETE':
        deleted = delete_one(PUBLIC_DATABASE, _type, logro_id)

        if not deleted:
            return jsonify({'message': 'Something went wrong'}), 500

        return jsonify({"redirect_to": f"/atletas/{athlete_id}/logros"}), 200

    try:
        atleta = next(iter(get_items('atletas', PUBLIC_DATABASE, filters=[
            {'field': 'id', 'values': [athlete_id]}])))
        logro = next(iter(get_items('logros', PUBLIC_DATABASE,
                                    filters=[{'field': 'id', 'values': [logro_id]}])))
    except Exception:
        return f"Logro con id {logro_id} no encontrado, <a href='/atletas/{athlete_id}/logros'>regresar</a>"

    return render_template('admin_atleta_logro.html', atleta=atleta, logro=logro)


@admin_blueprint.route('/atletas/<athlete_id>/logros/nuevo', methods=['GET', 'POST'])
@login_required
def admin_new_achievement_screen(athlete_id):
    """ Screen to add new milestone """
    _type = 'hito'
    if request.method == 'POST':
        added = add_one(PUBLIC_DATABASE, _type, request)
        if not added:
            return jsonify({'message': 'Something went wrong'}), 500

    atleta = next(iter(get_items('atletas', PUBLIC_DATABASE, filters=[
        {'field': 'id', 'values': [athlete_id]}])))
    return render_template('admin_atleta_logro.html', atleta=atleta)
