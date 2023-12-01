import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from celery import Celery
from celery import Task
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
from flask_security.models import fsqla_v3 as fsqla
from flask_mailman import Mail
from flask_babel import Babel, format_date, format_datetime
from flask_migrate import Migrate
from app.config import Development
from app.utils.forms import ExtendedRegisterForm


db = SQLAlchemy()
mail = Mail()
babel = Babel()
jwt = JWTManager()
migrate = Migrate()

def setup_logging(app):
    log_format = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')

    if app.debug:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_format)
        console_handler.setLevel(logging.DEBUG)
        app.logger.addHandler(console_handler)
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

def create_app() -> Flask:
    app = Flask(__name__)

    app.config.from_object(Development)

    db.init_app(app)
    mail.init_app(app)
    babel.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Setup logging
    setup_logging(app)
    app.logger.info('Webpage is starting up...')
    
    fsqla.FsModels.set_db_info(db)

    # To get the functions to jinja2
    app.jinja_env.globals['format_date'] = format_date
    app.jinja_env.globals['format_datetime'] = format_datetime
    app.jinja_env.globals['getattr'] = getattr
    app.jinja_env.add_extension('jinja2.ext.do')

    from app.users.models import User, Role  # noqa
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

    @app.context_processor
    def inject_hunt_years():
        from app.hunting.models import HuntYear #noqa
        from app.utils.hunt_year import HuntYearFinder
        from sqlalchemy import desc
        hunt_year = HuntYearFinder()
        current_hunt_year = hunt_year.current
        next_hunt_year = hunt_year.next()
        hunt_years = HuntYear.query.order_by(desc(HuntYear.name)).all()
        return  {
            'current_hunt_year': current_hunt_year,
            'next_hunt_year': next_hunt_year,
            'hunt_years': hunt_years
        }


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
    app.extensions["celery"] = celery_app
    return celery_app
