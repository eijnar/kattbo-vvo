from flask import Blueprint, redirect, url_for, render_template, request
from flask_security import current_user
from app.models.utils import Document
from markdown import markdown
from app.models.news import Post
from app.blueprints.hunting.utils import get_quota_statistics
from markdown import markdown


news = Blueprint('news', __name__, template_folder='templates')

@news.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for('news.news_page'))
    return redirect('/login')

@news.route('/news')
def news_page():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.created_at.desc()).paginate(page=page, per_page=5)
    for post in posts:
        post.content = markdown(post.content)
        print(post.content)
    return render_template('news/news.html.j2', posts=posts)


@news.route("/pm")
def pm():
    doc = Document.query.first()
    return render_template('markdown.html.j2', doc=markdown(doc.document))

@news.route("/statistics")
def statistics():
    statistics = get_quota_statistics(1)
    return render_template('news/stats.html.j2', statistics=statistics)