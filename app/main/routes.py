from flask import Blueprint, render_template
from flask_jwt_extended import create_access_token

main = Blueprint('main', __name__, template_folder='templates')

@main.route("/")
def home():
    return render_template("main/index.html.j2")