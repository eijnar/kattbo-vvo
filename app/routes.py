from app import app, db
from flask_security import auth_required, roles_accepted, current_user
from flask import render_template_string, render_template, flash
from app.models import User


@app.route("/")
def home():
    return render_template("main/index.html")