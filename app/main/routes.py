from flask_security import auth_required, roles_accepted, current_user
from flask import Blueprint render_template_string, render_template, flash

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return render_template("main/index.html")