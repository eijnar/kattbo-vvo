from flask import Blueprint, redirect, url_for, render_template, request
from flask_security import current_user
from app.utils.pdf import PDFCreator
from app.utils.models import Document
from markdown import markdown
from app.main.models import Post

main = Blueprint('main', __name__, template_folder='templates')


@main.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for('main.news'))
    return redirect('/login')


@main.route('/news')
def news():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.created_at.desc()).paginate(page=page, per_page=5)
    return render_template('main/news.html.j2', posts=posts)


@main.route("/pm")
def pm():
    doc = Document.query.first()
    return render_template('markdown.html.j2', doc=markdown(doc.document))

# @shared_task
# @main.route("/celery")
# def celery():
#     context = {
#         'variable1': 'Some data',
#         'variable2': 'Other data'
#     }

#     pdf_creator = PDFCreator('pdf/pdf_template.html.j2', 'test.pdf')

#     pdf_creator.generate_pdf(context=context)

#     return render_template_string('test')
