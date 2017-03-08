import os, pprint

from flask import Flask
from flask_bootstrap import Bootstrap

from .navbar import nav
from .models import db
from .frontend import frontend


def create_app(config):

    print("config = %s" % config)

    app = Flask(__name__)

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

    if app.config['PYQDBS_ENABLE_ADMIN']:
        from .admin import admin
        admin.init_app(app)

    app.register_blueprint(frontend)

    app.config['BOOTSTRAP_SERVE_LOCAL'] = True

    @app.cli.command("initdb")
    def initdb_command():
        """ Initialize the quote database """
        db.create_all()
        print("database initialized")

    return app
