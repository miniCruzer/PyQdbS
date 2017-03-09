from flask import current_app

from flask_wtf import FlaskForm
from wtforms import *

from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from PyQdbS.models import db

login_manager = LoginManager()
bcrypt = Bcrypt()

class Users(db.Model):

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    username = db.Column(db.String(), unique=True)
    password = db.Column(db.String())

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_id(self):
        return self.username

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

    def is_active(self):
        return True

    def __unicode__(self):
        return self.username

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

class LoginForm(FlaskForm):

    username = StringField("Username", [ validators.required() ])
    password = PasswordField("Password", [ validators.required() ])
    submit = SubmitField('Submit')

@login_manager.user_loader
def user_loader(user_id):
    return Users.query.filter(Users.username == user_id).first()
