from flask import Blueprint, render_template_string
from flask_security import auth_required, roles_accepted
from app.hunting.models import HuntTeam


hunting = Blueprint('hunting', __name__, template_folder='templates')


@hunting.route("/")
@auth_required
@roles_accepted('admin', 'hunter')
def home():
    hunt_team = HuntTeam.query.all()
    for i in hunt_team:
        print(i)
    return render_template_string(f"{hunt_team[0].name}")
