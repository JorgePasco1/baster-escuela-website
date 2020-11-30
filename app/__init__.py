import os

from flask import Flask, render_template, request, jsonify

from .admin import admin_blueprint
from .user import user_blueprint


def create_app():
    app = Flask(__name__)
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SERVER_NAME"] = os.environ.get('HOST') or "localhost:5000"
    app.register_blueprint(user_blueprint)
    app.register_blueprint(admin_blueprint, subdomain='admin')

    return app
