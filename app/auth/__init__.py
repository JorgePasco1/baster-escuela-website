"""
Authorization Blueprint (login, signup, logout)
"""

from flask import Blueprint, redirect, jsonify, render_template, request, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import urlparse, urlunparse

from app.models import User
from app import db

auth_blueprint = Blueprint('auth', __name__, template_folder='templates')


@auth_blueprint.route('/')
def home():
    return redirect('/login')


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    user = request.form.get('user')
    password = request.form.get('password')

    user = User.query.filter_by(user=user).first()

    if not user or not check_password_hash(user.password, password):
        flash('Usuario o Contraseña incorrectos. Intenta de nuevo')
        return redirect('/login')

    urlparts = urlparse(request.url)
    domain = urlparts.netloc.split('auth.')[1]
    admin_sub = f"admin.{domain}"

    urlparts_list = list(urlparts)
    urlparts_list[1] = admin_sub
    urlparts_list[2] = '/home'
    return redirect(urlunparse(urlparts_list), code=301)


# @auth_blueprint.route('/signup', methods=['POST'])
# def signup():
#     user = request.json.get('user')
#     password = request.json.get('password')
#     name = request.json.get('name')

#     new_user = User(user=user, password=generate_password_hash(password, method='sha256'), name=name)

#     db.session.add(new_user)
#     db.session.commit()
#     return jsonify({"success": True, "user": user})


@auth_blueprint.route('/logout')
def logout():
    return 'Logout'
