import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from celery import Celery, Task
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
from flask_security.models import fsqla_v3 as fsqla
from flask_mailman import Mail
from flask_babel import Babel, format_date, format_datetime
from flask_migrate import Migrate
from app.config import Development
from app.utils.forms import ExtendedRegisterForm
from elasticapm.contrib.flask import ElasticAPM
import elasticapm


db = SQLAlchemy()
mail = Mail()
babel = Babel()
jwt = JWTManager()
migrate = Migrate()
celery = Celery()
apm = ElasticAPM()

def create_app() -> Flask:
    app = Flask(__name__)

    app.config.from_object(Development)
    app.config.from_prefixed_env()

    db.init_app(app)
    mail.init_app(app)
    babel.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    celery_init_app(app)
    apm.init_app(app)

    # Setup logging
    setup_logging(app)
    app.logger.info('Webpage is starting up...')
    
    #fsqla.FsModels.set_db_info(db)
    from app.users.models import User, Role  # noqa

    # To get the functions to jinja2
    app.jinja_env.globals['format_date'] = format_date
    app.jinja_env.globals['format_datetime'] = format_datetime
    app.jinja_env.globals['getattr'] = getattr
    app.jinja_env.add_extension('jinja2.ext.do')

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, user_datastore, register_blueprint=True,
                            confirm_register_form=ExtendedRegisterForm)

    from app.tag.routes import tags
    app.register_blueprint(tags, url_prefix='/tags')

    from app.users.routes import users
    app.register_blueprint(users, url_prefix='/user')

    from app.events.routes import events
    app.register_blueprint(events, url_prefix='/events')

    from app.main.routes import main
    app.register_blueprint(main)

    from app.utils.routes import utils
    app.register_blueprint(utils)

    from app.hunting.routes import hunting
    app.register_blueprint(hunting, url_prefix='/jakt')

    from app.admin.routes import admin
    app.register_blueprint(admin, url_prefix='/admin')

    from app.map.routes import map
    app.register_blueprint(map, url_prefix='/map')

    from app.errors.handlers import errors
    app.register_blueprint(errors)

    from app.api.routes import api
    app.register_blueprint(api, url_prefix='/api')

    # Custom URL shortening with JTW tokens. This function is mainly used for
    # quick registration
    from app.utils.urlshorter import URLShortener  # noqa
    app.urlshortener = URLShortener(
        base_url='https://dev.kattbovvo.se',
        registration_route='/events/quick_registration'
    )


    # At last, create the database structure within the construct.
    with app.app_context():
        db.create_all()
        
    return app


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    return celery_app


def setup_logging(app):
    log_format = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')

    if not app.logger.handlers:
        if app.debug:
            file_handler = RotatingFileHandler('kattbo_vvo_dev_flask.log', maxBytes=10240, backupCount=10)
            file_handler.setFormatter(log_format)
            file_handler.setLevel(logging.DEBUG)
            app.logger.addHandler(file_handler)
        else:
            file_handler = RotatingFileHandler('kattbo_vvo_flask.log', maxBytes=10240, backupCount=10)
            file_handler.setFormatter(log_format)
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.DEBUG if app.debug else logging.INFO)