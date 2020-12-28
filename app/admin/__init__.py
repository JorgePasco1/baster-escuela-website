"""
Admin Blueprint
"""
import os
from werkzeug.utils import secure_filename

from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from app.common.database import get_items, add_new_item_to_db, update_record_in_db, \
    delete_record_in_db
from app.admin.crud_factory import update_one, delete_one, add_one
from app.common.constants import PUBLIC_DATABASE

admin_blueprint = Blueprint('admin', __name__, template_folder='templates',
                            static_folder='static', static_url_path='/app/admin/static')


# pylint: disable=wrong-import-position
from app.admin.routes import achievements, atletas, directiva, trainers, hitos


@admin_blueprint.route('/')
def admin_redirect():
    """ Redirect '/' route to /home """
    return redirect(url_for('.admin_index'))


@admin_blueprint.route('/home')
@login_required
def admin_index():
    """ Homepage for admins """
    return render_template('admin_home.html', user_name=current_user.name)
