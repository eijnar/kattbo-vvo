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
    migrate.init_app(app, db)
    celery_init_app(app)
    
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
    app.register_blueprint(admin, url_prefix='/admins')

    from app.errors.handlers import errors
    app.register_blueprint(errors)

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

    # data = urllib.request.urlopen('https://api.namnapi.se/v2/names.json?limit=20').read()
    # data = json.loads(data)
    # def random_with_N_digits(n):
    #     range_start = 10**(n-1)
    #     range_end = (10**n)-1
    #     return random.randint(range_start, range_end)

    # for i in data['names']:
    #     rand_mail = ''.join(random.choice("abcdefghijklmnopqrstyv") for _ in range(6))
    #     # rand_phone = f'070{random_with_N_digits(7)}'
    #     r_email = rand_mail + "@kaffesump.se"
    #     r_first_name = i['firstname']
    #     r_last_name = i['surname']
    #     r_phone_number = f'070{random_with_N_digits(7)}'

    #     # print(r_email, r_phone_number, r_first_name, r_last_name)
    #     app.security.datastore.create_user(email=r_email, first_name=r_first_name, last_name=r_last_name, phone_number=r_phone_number)
        db.session.commit()
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
