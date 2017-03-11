# adjust the Config class below, then rename this file to config.py

class DefaultConfig(object):
    # a decent way to generate a secret key is by running: python -c "import os; print(repr(os.urandom(24)))"
    # then pasting the output here.
    SECRET_KEY                      = __NOT_SET__

    # how many quotes to display per page before paginating
    PYQDBS_QUOTES_PER_PAGE          = 15

    # enable the Admin interface? creates an /admin page
    PYQDBS_ENABLE_ADMIN             = True

    # enable the RESTful API? served on /api, can be used to add/retrieve quotes easily via an IRC bot or something
    PYQDBS_ENABLE_RESTFUL_API       = True

    # enable the reCAPTCHA form on the add quotes page?
    PYQDBS_ENABLE_RECAPTCHA         = False

    # set these to your own values if you want to enable the reCAPTCHA form when submitting quotes
    RECAPTCHA_PUBLIC_KEY            = None
    RECAPTCHA_PRIVATE_KEY           = None

    PQYDBS_PPRINT_CONFIG            = False

    DEBUG                           = False
    TESTING                         = False

    SQLALCHEMY_TRACK_MODIFICATIONS  = False
    SQLALCHEMY_DATABASE_URI         = "sqlite:///:memory:"

class ProductionConfig(DefaultConfig):
    # use the default SQLite database
    SQLALCHEMY_DATABASE_URI         = "sqlite:///../qdbs.db"

    # or if you'd rather use PostgreSQL you can do that too.
    # this assumes there's a database called "qdbs"
    # use the 'createdb' command provided by your postgres install
    # to create an actual database.

    #SQLALCHEMY_DATABASE_URI         = "postgres://localhost/qdbs"


class DevelopmentConfig(ProductionConfig):
    DEBUG                           = True
    TESTING                         = True
    SQLALCHEMY_TRACK_MODIFICATIONS  = True
