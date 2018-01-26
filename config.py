import os
basedir = os.path.abspath(os.dirname(__file__))

class Config(object):

    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY =
    SQLALCHEMY_DATABASE_URI = os.envrion.get('DATABASE_URL', 'sqlite:///catalog2.db')

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    TESTING = True