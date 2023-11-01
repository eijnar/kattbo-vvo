from flask import Flask, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, auth_required, hash_password, UserDatastore, user_registered
from flask_security.models import fsqla_v3 as fsqla
from flask_mailman import Mail
from flask_marshmallow import Marshmallow
from flask_babel import Babel, format_date, format_datetime
from app.config import Development

db = SQLAlchemy()
mail = Mail()
babel = Babel()

def create_app()
    app = Flask(__name__)

    app.config.from_object(Development)

    db.init_app(app)
    fsqla.FsModels.set_db_info(db)

    db.init_app(app)
    mail.init_app(app)
    babel.init_app(app)

    app.jinja_env.globals['format_date'] = format_date
    app.jinja_env.globals['format_datetime'] = format_datetime

    from app.users.models import User, Role  # noqa
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, user_datastore)

    from app.users.routes import users
    from app.admin.routes import admin
    from app.events.routes import events
    from app.main.routes import main
    app.register_blueprint(users)
    app.register_blueprint(admin)
    app.register_blueprint(events)
    app.register_blueprint(main)

    # Add all registered users to the default 'user' role
    #@user_registered.connect_via(app)
    #def user_registered_sighandler(sender, user, **extra):
    #    default_role = Role.query.filter_by(name='user').first()
    #    user.roles.append(default_role)
    #    db.session.commit()

    # Make sure that that all databases are accounted for
    with app.app_context():
        db.create_all()

    return app