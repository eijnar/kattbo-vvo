from flask import Blueprint, redirect, url_for, render_template, request
from app import db
from flask_security import current_user
from models.utils import Document
from markdown import markdown
from models.news import Post
from app.blueprints.hunting.utils import get_quota_statistics
from app.blueprints.news.forms import PostForm
from markdown import markdown


news = Blueprint('news', __name__, template_folder='templates')

@news.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for('news.news_page'))
    return redirect('/login')

@news.route('/news', methods=['GET'])
def news_page():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.created_at.desc()).paginate(page=page, per_page=5)
    for post in posts:
        post.content = markdown(post.content)
    return render_template('news/news.html.j2', posts=posts)

@news.route('/news/post', methods=['GET', 'POST'])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(
            title = form.title.data,
            content = form.content.data,
            user_id = current_user.id
        )
        db.session.add(new_post)
        db.session.commit()

    return render_template('news/new_post.html.j2', form=form)


@news.route("/pm")
def pm():
    doc = Document.query.first()
    return render_template('markdown.html.j2', doc=markdown(doc.document))

@news.route("/statistics")
def statistics():
    statistics = get_quota_statistics(1)
    return render_template('news/stats.html.j2', statistics=statistics)