from flask import Flask, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, auth_required, hash_password, UserDatastore
from flask_security.models import fsqla_v3 as fsqla
from flask_mailman import Mail
from flask_marshmallow import Marshmallow
from config import Development



app = Flask(__name__)
app.config.from_object('config.Development')

db = SQLAlchemy(app)
mail = Mail(app)
ma = Marshmallow(app)

fsqla.FsModels.set_db_info(db)

from app.models import User, Role

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
app.security = Security(app, user_datastore)
usr = UserDatastore(User, Role)

from app import routes #noqa
from app.user import routes #noqa
from app.admin import routes #noqa