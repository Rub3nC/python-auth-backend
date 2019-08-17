import os


basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecret')
    DEBUG = False


class DevelopmentConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'auth-backend-main.db')


class TestingConfig:
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'auth-backend-test.db')


class ProductionConfig:
    DEBUG = False


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
    