import os


class Config(object):
    """
    Set Flask configuration variables.
    """

    # Default mail configuration
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_DEFAULT_SENDER = 'Kättbo VVO'

    # Flask-WTF Secret key
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # TimeZone and locale settings
    BABEL_DEFAULT_LOCALE = 'sv'
    BABEL_DEFAULT_TIMEZONE = 'Europe/Stockholm'

    # Flask-Security-Too settings
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT')
    SECURITY_PASSWORD_HASH = os.environ.get('SECURITY_PASSWORD_HASH')
    SECURITY_TRACKABLE = os.environ.get('SECURITY_TRACKABLE')

    # Flask-Security-Too registration settings
    SECURITY_REGISTERABLE = os.environ.get('SECURITY_REGISTERABLE')
    SECURITY_CONFIRMABLE = os.environ.get('SECURITY_CONFIRMABLE')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM')


class Development(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

    # Flask-Security-Too settings
    SECURITY_EMAIL_VALIDATOR_ARGS = {"check_deliverability": False}
    
    # Mailman dev. configuration
    MAIL_DEFAULT_SENDER = 'Kättbo VVO', 'development@kaffesump.se'

class Production(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')