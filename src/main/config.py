import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
dotenv_path = os.path.join('{}/src/'.format(basedir), '.env')
load_dotenv(dotenv_path)

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecret')
    DEBUG = False
    PROPAGATE_EXCEPTIONS = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AUTH_PASSWORD_VALIDATORS_PARAMETERS = {
        "length": 8,        # Min length: 8            
        "uppercase": 0,     # Need min. 0 uppercase letters 
        "numbers": 1,       # Need min. 1 digits
        "special": 1,       # Need min. 1 special characters
        "strength": 0       # password strength. Value range [0 : 1]
    }

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

    # The options are mailgun, sendgrid or print in console.
    # If you select mailgun you must provide the information of MAILGUN_API_KEY and MAILGUN_DOMAIN
    # If you select sendgrid you must provide the information of SENDGRID_API_KEY
    # Else print the email in the console
    EMAIL_BACKEND = "console"

    MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY", None)
    MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN", None)
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", None)

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
    