from app.blueprints.tag import tags
from flask_security import login_required, roles_accepted, login_required
from flask import Blueprint

tags = Blueprint('tags', __name__, template_folder='templates')

@tags.route("/tagadfs/delete/<int:id>", methods=['POST'])
@login_required
def andom_delete_tag(id):
    pass


@tags.route("/buklknindsf", methods=['GET', 'POST'])
@login_required
@roles_accepted("hunter")
def tags_admin():
    pass
