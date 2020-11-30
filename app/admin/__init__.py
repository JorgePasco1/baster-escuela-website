from flask import Blueprint, render_template

admin_blueprint = Blueprint('admin', __name__, template_folder='templates/')

@admin_blueprint.route('/')
def admin_index():
    return render_template('admin_login.html')