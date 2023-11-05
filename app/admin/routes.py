from flask_security import auth_required, roles_accepted
from flask import Blueprint, render_template
from app.users.models import User
from app.events.models import Event
from app.tag.models import Tag

admin = Blueprint('admin', __name__, template_folder='templates')

@admin.route("/users")
def list_users():
    users = User.list_all()
    page_title = 'Administrera användare'
    return render_template('default_list_all.html.j2', items=users, page_title=page_title)

@admin.route('/events')
def list_events():
    events = Event.list_all()
    page_title = 'Administrera händelser'
    return render_template('default_list_all.html.j2', items=events, page_title=page_title)

@admin.route('/tags')
def list_tagss():
    events = Tag.list_all()
    page_title = 'Administrera tags'
    return render_template('default_list_all.html.j2', items=events, page_title=page_title)