from flask import Blueprint

tags = Blueprint('tags', __name__, template_folder='templates')

from app.blueprints.tag import routes