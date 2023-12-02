from flask import Blueprint, redirect, url_for, render_template, request
from flask_security import current_user
from celery import shared_task
from app.utils.models import Document
from markdown import markdown
from app.main.models import Post
from app.hunting.models import AnimalQuota
from time import sleep

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

@main.route("/statistics")
def statistics():

    def get_quota_statistics(hunt_year_id):
        quotas = AnimalQuota.query.filter_by(hunt_year_id=hunt_year_id).all()
        statistics = {}

        for quota in quotas:
            team_name = quota.hunt_team.name
            animal_name = quota.animal_type.name
            remaining_quota = quota.initial_quota - len(quota.animals_shot)

            if team_name not in statistics:
                statistics[team_name] = {}

            statistics[team_name][animal_name] = remaining_quota
            
        return statistics

    statistics = get_quota_statistics(1)

    return render_template('main/stats.html.j2', statistics=statistics)



@main.route("/celery")
def celery():
    print("test")
    wait.delay()
    return "hej"

@shared_task
def wait():
    sleep(10)
    return True