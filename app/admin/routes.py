from flask_security import auth_required, roles_accepted
from flask import Blueprint, render_template
from app.users.models import User

admin = Blueprint('admin', __name__, template_folder='templates')

@admin.route("/admin/users")
@auth_required()
@roles_accepted('superadmin', 'admin')
def admin_users():
    users = User.query.all()
    return render_template('admin/users.html.j2', users=users)