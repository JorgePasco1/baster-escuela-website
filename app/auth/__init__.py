"""
Authorization Blueprint (login, logout)
"""

from flask import Blueprint, redirect, render_template, request, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app import db

auth_blueprint = Blueprint('auth', __name__, template_folder='templates')


@auth_blueprint.route('/')
def home():
    redirect('/login')


@auth_blueprint.route('/login')
def login():
    return render_template('login.html')


@auth_blueprint.route('/logout')
def logout():
    return 'Logout'
