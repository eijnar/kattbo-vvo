from flask import Flask
from celery import Celery
from celery import Task
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, auth_required, hash_password, UserDatastore, user_registered
from flask_security.models import fsqla_v3 as fsqla
from flask_mailman import Mail
from flask_babel import Babel, format_date, format_datetime
from app.config import Development
from app.utils.forms import ExtendedRegisterForm


db = SQLAlchemy()
mail = Mail()
babel = Babel()
jwt = JWTManager()


def create_app() -> Flask:
    app = Flask(__name__)

    app.config.from_object(Development)
    app.config.from_mapping(
        CELERY=dict(
            broker_url="amqp://vvo_celery:dp58nYaiJM8ymNEdebj5s8eqc4vzCJn@vvo.srv.kaffesump.se:5672/kattbo_vvo",
            result_backend="db+mysql://kattbo_vvo_celery:Aj8Ze5etTeYTX8qMHd2MfxZYKzH5wqU@172.30.149.3/kattbo_vvo_celery",
            task_ignore_result=True,
        ),
    )

    db.init_app(app)
    mail.init_app(app)
    babel.init_app(app)
    jwt.init_app(app)
    celery_init_app(app)

    # fsqla.FsModels.set_db_info(db)

    # To get the functions to jinja2
    app.jinja_env.globals['format_date'] = format_date
    app.jinja_env.globals['format_datetime'] = format_datetime
    app.jinja_env.globals['getattr'] = getattr

    from app.users.models import User, Role  # noqa
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, user_datastore, confirm_register_form=ExtendedRegisterForm)
    
    from app.users.routes import users
    from app.events.routes import events
    from app.main.routes import main
    from app.utils.routes import utils
    from app.tag.routes import tags
    app.register_blueprint(tags)
    app.register_blueprint(main)
    app.register_blueprint(utils)
    app.register_blueprint(users, url_prefix='/user')
    app.register_blueprint(events, url_prefix='/events')

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
    app.extensions["celery"] = celery_app
    return celery_app
