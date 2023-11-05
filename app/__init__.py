from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, auth_required, hash_password, UserDatastore, user_registered
from flask_security.models import fsqla_v3 as fsqla
from flask_mailman import Mail
from flask_babel import Babel, format_date, format_datetime
from app.config import Development


db = SQLAlchemy()
mail = Mail()
babel = Babel()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    app.config.from_object(Development)

    db.init_app(app)
    mail.init_app(app)
    babel.init_app(app)
    jwt.init_app(app)

    fsqla.FsModels.set_db_info(db)

    # To get the functions to jinja2
    app.jinja_env.globals['format_date'] = format_date
    app.jinja_env.globals['format_datetime'] = format_datetime
    app.jinja_env.globals['getattr'] = getattr

    from app.users.models import User, Role  # noqa
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, user_datastore)

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
        base_url='http://127.0.0.1:5000',
        registration_route='/events/quick_registration'
    )

    # At last, create the database structure within the construct.
    with app.app_context():
        db.create_all()

    return app
