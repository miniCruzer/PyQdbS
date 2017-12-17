import os

class DefaultConfig(object):
    SECRET_KEY                      = os.environ["SECRET_KEY"]

    PYQDBS_QUOTES_PER_PAGE          = 2
    PYQDBS_ENABLE_ADMIN             = True
    PYQDBS_ENABLE_RESTFUL_API       = True
    PYQDBS_ENABLE_RECAPTCHA         = False
    PYQDBS_ENABLE_RESTAPI           = True
    PYQDBS_PPRINT_CONFIG            = False

    RECAPTCHA_PUBLIC_KEY            = os.environ["RECAPTCHA_PUBLIC_KEY"]
    RECAPTCHA_PRIVATE_KEY           = os.environ["RECAPTCHA_PRIVATE_KEY"]

    DEBUG                           = False
    TESTING                         = False

    SQLALCHEMY_TRACK_MODIFICATIONS  = False
    SQLALCHEMY_DATABASE_URI         = "sqlite:///:memory:"

class ProductionConfig(DefaultConfig):
    SQLALCHEMY_DATABASE_URI         = os.environ["DATABASE_URL"]

class DevelopmentConfig(ProductionConfig):
    DEBUG                           = True
    TESTING                         = True
    SQLALCHEMY_ECHO                 = False
    PYQDBS_PPRINT_CONFIG            = False
