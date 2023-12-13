from os import environ


class Config(object):
    """
    Set Flask configuration variables.
    """

    UPLOAD_FOLDER = environ.get('UPLOAD_FOLDER')

    # Default mail configuration
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
    MAIL_PORT = environ.get('MAIL_PORT')
    MAIL_USE_SSL = environ.get('MAIL_USE_SSL')
    MAIL_SERVER = environ.get('MAIL_SERVER')
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

    API_BASE = 'https://api.kattbovvo.se'

    # Celery 
    CELERY = dict(
        broker_url=environ.get('CELERY_BROKER_URL'),
        result_backend=environ.get('CELERY_BACKEND_URL'),
        task_ignore_result=False,
        task_serializer='pickle',
        result_serializer='pickle',
        accept_content=['pickle', 'application/x-python-serialize', 'json'],
    )

    # Elastic APM
    ELASTIC_APM = {
        'SERVICE_NAME': 'kattbo-vvo-web',
        'SERVER_URL': 'http://riker.srv.kaffesump.se:8200/',
        'SECRET_TOKEN': 'tYeW2uFgP6JfcbUzkkqU7xur9i5DKPHMnRzqE',
        'ENVIRONMENT': 'development',
    }

class Development(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI_DEV')

    # Flask-Security-Too settings
    SECURITY_EMAIL_VALIDATOR_ARGS = {"check_deliverability": False}
    
    # Mailman dev. configuration
    MAIL_DEFAULT_SENDER = "dev@kattbovvo.se"


class Production(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI_PROD')