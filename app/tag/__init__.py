from flask import Blueprint

tags = Blueprint('tags', __name__, template_folder='templates')

from app.tag import routes