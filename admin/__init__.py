from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

admin_blueprint = Blueprint('admin', __name__, template_folder='templates')

@admin_blueprint.route('/')
def admin_index():
    return "Hello, admin"