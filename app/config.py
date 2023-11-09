from os import environ


class Config(object):
    """
    Set Flask configuration variables.
    """

    # Default mail configuration
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_SERVER = environ.get('MAIL_SERVER')
    MAIL_DEFAULT_SENDER = 'Kättbo VVO'

    # Flask-WTF Secret key
    SECRET_KEY = environ.get('SECRET_KEY')

    # TimeZone and locale settings
    BABEL_DEFAULT_LOCALE = 'sv'
    BABEL_DEFAULT_TIMEZONE = 'Europe/Stockholm'

    # Flask-Security-Too settings
    SECURITY_PASSWORD_SALT = environ.get('SECURITY_PASSWORD_SALT')
    SECURITY_PASSWORD_HASH = environ.get('SECURITY_PASSWORD_HASH')
    SECURITY_TRACKABLE = environ.get('SECURITY_TRACKABLE')

    # Flask-Security-Too registration settings
    SECURITY_REGISTERABLE = environ.get('SECURITY_REGISTERABLE')
    SECURITY_CONFIRMABLE = environ.get('SECURITY_CONFIRMABLE')
    JWT_SECRET_KEY = environ.get('JWT_SECRET_KEY')
    JWT_ALGORITHM = environ.get('JWT_ALGORITHM')


class Development(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')

    # Flask-Security-Too settings
    SECURITY_EMAIL_VALIDATOR_ARGS = {"check_deliverability": False}
    
    # Mailman dev. configuration
    MAIL_DEFAULT_SENDER = 'Kättbo VVO', 'development@kaffesump.se'

class Production(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
