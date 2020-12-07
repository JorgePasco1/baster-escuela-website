"""
Admin Blueprint
"""

from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


@admin_blueprint.route('/')
def admin_redirect():
    """ Redirect '/' route to /home """
    return redirect(url_for('.admin_index'))


@admin_blueprint.route('/home')
@login_required
def admin_index():
    """ Homepage for admins """
    return render_template('admin_home.html', user_name=current_user.name)
