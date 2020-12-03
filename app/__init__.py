"""
Main Application

Functions: create_app
"""

import os

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

# pylint: disable=wrong-import-position
from .auth import auth_blueprint
from .user import user_blueprint
from .admin import admin_blueprint

def create_app():
    """ Create Flask Application """
    app = Flask(__name__)
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SERVER_NAME"] = os.environ.get('HOST') or "localhost:5000"
    app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///admin.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(user_blueprint)
    app.register_blueprint(admin_blueprint, subdomain='admin')
    app.register_blueprint(auth_blueprint, subdomain='auth')
    # login_manager = start_login_manager(app)

    return app
