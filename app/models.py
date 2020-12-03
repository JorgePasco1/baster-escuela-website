"""
Database Models
"""

from app import db

class User(db.Model):
    """ User Model """
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
