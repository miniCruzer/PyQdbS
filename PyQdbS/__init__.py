import os
import pprint

from flask import Flask
from flask_bootstrap import Bootstrap

from .frontend import frontend
from .models import db
from .navbar import nav


def create_app(config):

    app = Flask(__name__)

    app.logger.info("using config {}".format(config))

    # load config

    app.config.from_object(__name__)
    app.config.from_object("PyQdbS.config.{}".format(config))
    app.config['DEBUG'] = 1

    if app.config.get('PYQDBS_PPRINT_CONFIG', False):
        pprint.pprint(app.config)

    # register plugins
    Bootstrap(app)
    nav.init_app(app)
    db.init_app(app)

    if app.config.get('PYQDBS_ENABLE_ADMIN', False):
        from .admin import admin
        from .auth import bcrypt, login_manager

        bcrypt.init_app(app)
        login_manager.init_app(app)
        admin.init_app(app)

        @app.cli.command("admin")
        def create_admin():
            """ creates an admin user """
            import string
            import secrets
            from .auth import Users

            passwd = "".join(
                secrets.choice(string.ascii_letters + string.digits) for i in range(12))

            hashedpw = bcrypt.generate_password_hash(passwd).decode() # decode this since PostgreSQL doesn't store unicode the same as SQLite.
            u = Users("admin", hashedpw, make_admin=True)
            Users.query.filter(Users.username == "admin").delete()

            db.session.add(u)
            db.session.commit()

            print(f"username: admin\npassword: {passwd}")

    if app.config.get('PYQDBS_ENABLE_RESTAPI', False):
        from .restapi import api
        api.init_app(app)

    app.register_blueprint(frontend)

    app.config['BOOTSTRAP_SERVE_LOCAL'] = True

    @app.cli.command("initdb")
    def initdb_command():
        """ Initialize the quote database """
        db.create_all()
        print("database initialized")

    return app
