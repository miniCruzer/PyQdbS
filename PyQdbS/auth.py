import base64
import os

from flask import current_app
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from itsdangerous import Signer
from wtforms import *

from PyQdbS.models import db

login_manager = LoginManager()
login_manager.session_protection = "strong"
bcrypt = Bcrypt()

# NOTE: BcryptPasswordField is here, and not in forms.py, because if you don't load
# the admin interface, then you don't need Bcrypt, which is required to build this form.
class BcryptPasswordField(PasswordField):
    def process_formdata(self, valuelist):
        value = ''
        if valuelist:
            value = valuelist[0]

        if value:
            self.data = bcrypt.generate_password_hash(value).decode()
        else:
            self.data = self.orig_hash

    def process_data(self, value):
        self.data = ''
        self.orig_hash = value


class Users(db.Model):

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    session_token = db.Column(db.String(), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean(), default=False)
    allow_api = db.Column(db.Boolean(), default=False)

    def __init__(self, username=None, password=None, make_admin=False, allow_api=False):
        self.username = username
        self.password = password

        self.is_admin = make_admin
        self.allow_api = allow_api

        self.make_session_token()

    def __repr__(self):
        return f'<User {self.username}>'

    def get_id(self):
        return self.session_token

    def get_username(self):
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

    def has_admin(self):
        return self.is_admin

    def can_api(self):
        return self.allow_api

    def make_session_token(self):
        signer = Signer(current_app.config["SECRET_KEY"])
        t= base64.b64encode(os.urandom(24))
        current_app.logger.debug(f"created a session token type {type(t)}: {t}")
        self.session_token = signer.sign(t).decode()

@login_manager.user_loader
def user_loader(session_token):
    signer = Signer(current_app.config["SECRET_KEY"])

    # verify the token we're getting hasn't been tampered with.
    if not signer.validate(session_token):
        current_app.logger.critical(f"bad signature from user's session token: {session_token}")
        return

    u =  Users.query.filter(Users.session_token == str(session_token)).first()
    if u:
        # verify token to make sure it hasn't been tampered with while in the database
        if not signer.validate(u.session_token):
            current_app.logger.critical(
                f"bad signature from stored session token: {u.session_token}")
            return

        current_app.logger.debug(
            f"loaded user by session token. user: {u} token: {u.session_token}")
        return u
