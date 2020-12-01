import os

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from .admin import admin_blueprint
from .admin.login import start_login_manager
from .user import user_blueprint
from .models import User

db = SQLAlchemy()


def create_app():
    """ Create Flask Application """
    app = Flask(__name__)
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SERVER_NAME"] = os.environ.get('HOST') or "localhost:5000"
    app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///admin.sqlite'

    db.init_app(app)

    app.register_blueprint(user_blueprint)
    app.register_blueprint(admin_blueprint, subdomain='admin')
    # login_manager = start_login_manager(app)

    return app
