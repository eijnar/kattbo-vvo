from flask import Blueprint

vvo = Blueprint('vvo', __name__, template_folder='templates')

@vvo.route('/files')
def vvo_files():
    pass
