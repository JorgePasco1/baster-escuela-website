"""
Authorization Blueprint (login, signup, logout)
"""
from urllib.parse import urlparse, urlunparse

from flask import Blueprint, redirect, jsonify, render_template, request, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import login_user, logout_user, login_required

from app.models import User
from app import db

auth_blueprint = Blueprint('auth', __name__, template_folder='templates')


@auth_blueprint.route('/')
def home():
    """ Redirect '/' route to /login """
    return redirect('/login')


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """ Login to the application """
    if request.method == 'GET':
        return render_template('login.html')

    user = request.form.get('user')
    password = request.form.get('password')

    user = User.query.filter_by(user=user).first()

    if not user or not check_password_hash(user.password, password):
        flash('Usuario o Contraseña incorrectos. Intenta de nuevo')
        return redirect('/login')

    login_user(user)
    return redirect(url_for('admin.admin_index'))


# @auth_blueprint.route('/signup', methods=['POST'])
# def signup():
#     user = request.json.get('user')
#     password = request.json.get('password')
#     name = request.json.get('name')

#     new_user = User(user=user, password=generate_password_hash(password, method='sha256'),
#       name=name)

#     db.session.add(new_user)
#     db.session.commit()
#     return jsonify({"success": True, "user": user})


@auth_blueprint.route('/logout')
@login_required
def logout():
    """ Logout of the application """
    logout_user()
    urlparts = urlparse(request.url)
    domain = urlparts.netloc.split('auth.')[1]
    auth_sub = f"auth.{domain}"

    urlparts_list = list(urlparts)
    urlparts_list[1] = auth_sub
    urlparts_list[2] = '/login'
    return redirect(urlunparse(urlparts_list), code=302)
