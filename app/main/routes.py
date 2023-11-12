from flask import Blueprint, render_template, redirect, url_for
from flask_security import LoginForm, current_user
from time import sleep
from app.utils.pdf import PDFCreator

main = Blueprint('main', __name__, template_folder='templates')

@main.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for('events.create_event'))
    login_form = LoginForm()
    return redirect('/login')

# @shared_task
# @main.route("/celery")
# def celery():
#     context = {
#         'variable1': 'Some data',
#         'variable2': 'Other data'
#     }

#     pdf_creator = PDFCreator('pdf/pdf_template.html.j2', 'test.pdf')

#     pdf_creator.generate_pdf(context=context).delay

#     return render_template_string('test')