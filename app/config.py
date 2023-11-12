from os import environ
from app.utils.forms import ExtendedRegisterForm


class Config(object):
    """
    Set Flask configuration variables.
    """

    # Default mail configuration
    MAIL_USERNAME = "eijnar@fastmail.com"
    MAIL_PASSWORD = "nmvlsb8vt38e9faf"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_SERVER = "smtp.fastmail.com"
    MAIL_DEFAULT_SENDER = "dev@kattbovvo.se"

    # Flask-WTF Secret key
    SECRET_KEY = environ.get('SECRET_KEY')

    # TimeZone and locale settings
    BABEL_DEFAULT_LOCALE = 'sv'
    BABEL_DEFAULT_TIMEZONE = 'Europe/Stockholm'

    # Flask-Security-Too settings
    SECURITY_PASSWORD_SALT = environ.get('SECURITY_PASSWORD_SALT')
    SECURITY_PASSWORD_SINGLE_HASH  = environ.get('SECURITY_PASSWORD_HASH')
    SECURITY_PASSWORD_SINGLE = environ.get('SECURITY_PASSWORD_HASH')
    SECURITY_TRACKABLE = environ.get('SECURITY_TRACKABLE')

    # Flask-Security-Too registration settings
    SECURITY_REGISTERABLE = environ.get('SECURITY_REGISTERABLE')
    SECURITY_CONFIRMABLE = environ.get('SECURITY_CONFIRMABLE')
    SECURITY_AUTO_LOGIN_AFTER_CONFIRM = True
    JWT_SECRET_KEY = environ.get('JWT_SECRET_KEY')
    JWT_ALGORITHM = environ.get('JWT_ALGORITHM')


class Development(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://kattbovvo_web:6QdEUA7p3t2ZBKngQXh8bW5h@172.30.149.3/kattbovvo_web_dev"

    # Flask-Security-Too settings
    SECURITY_EMAIL_VALIDATOR_ARGS = {"check_deliverability": False}
    
    # Mailman dev. configuration
    MAIL_DEFAULT_SENDER = "dev@kattbovvo.se"

class Production(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI_PROD')