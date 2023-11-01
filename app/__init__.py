from flask import Flask, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, auth_required, hash_password, UserDatastore, user_registered
from flask_security.models import fsqla_v3 as fsqla
from flask_mailman import Mail
from flask_marshmallow import Marshmallow
from flask_babel import Babel
from config import Development


app = Flask(__name__)
app.config.from_object('config.Development')
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
db = SQLAlchemy(app)
mail = Mail(app)
ma = Marshmallow(app)
babel = Babel(app)

fsqla.FsModels.set_db_info(db)

from app.models import User, Role  # noqa

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
app.security = Security(app, user_datastore)
usr = UserDatastore(User, Role)
babel.init_app(app)

# Routes to import
from app import routes  # noqa
from app.user import routes  # noqa
from app.admin import routes  # noqa
from app.event import routes  # noqa

# Add all registered users to the default 'user' role
#@user_registered.connect_via(app)
#def user_registered_sighandler(sender, user, **extra):
#    default_role = Role.query.filter_by(name='user').first()
#    user.roles.append(default_role)
#    db.session.commit()

# Make sure that that all databases are accounted for
with app.app_context():
    db.create_all()
