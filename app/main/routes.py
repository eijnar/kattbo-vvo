from flask import Blueprint, redirect, url_for, render_template, render_template_string
from flask_security import current_user
from app.utils.pdf import PDFCreator
from app.utils.models import Document
from markdown import markdown

main = Blueprint('main', __name__, template_folder='templates')


@main.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for('events.list_events'))
    return redirect('/login')


@main.route("/pm")
def pm():
    doc = Document.query.first()
    print
    return render_template('markdown.html.j2', doc=markdown(doc.document))

# @shared_task
@main.route("/celery")
def celery():
    context = {
        'variable1': 'Some data',
        'variable2': 'Other data'
    }

    pdf_creator = PDFCreator('pdf/pdf_template.html.j2', 'test.pdf')

    pdf_creator.generate_pdf(context=context)

    return render_template_string('test')
