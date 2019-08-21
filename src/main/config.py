import os


basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecret')
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    ACCOUNT_EMAIL_REQUIRED=True
    # -------------------------------------------------------------------------------------------------
    # The options are username, email or username_email. For email and username_email
    # Setting this to “email” requires ACCOUNT_EMAIL_REQUIRED=True
    ACCOUNT_AUTHENTICATION_METHOD = 'username'
    # -------------------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------
    # The options are mandatory, optional or none
    # Setting this to “mandatory” requires ACCOUNT_EMAIL_REQUIRED to be True
    # When set to “mandatory” the user is blocked from logging in until the email address is verified. 
    # Choose “optional” or “none” to allow logins with an unverified e-mail address. 
    # In case of “optional”, the e-mail verification mail is still sent, 
    # whereas in case of “none” no e-mail verification mails are sent.
    ACCOUNT_EMAIL_VERIFICATION = 'optional'
    # -------------------------------------------------------------------------------------------------
    ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'auth-backend-main.db')
    

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'auth-backend-test.db')


class ProductionConfig(Config):
    DEBUG = False


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
    