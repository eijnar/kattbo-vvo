from app import app, db, user_datastore, usr
from flask_security import auth_required, roles_accepted, current_user, permissions_accepted
from flask import render_template_string, redirect, url_for, flash, request, render_template, jsonify
from app.models import User, Role

@app.route('/admin/roles/<int:user_id>', methods=['GET', 'POST'])
def roles(user_id):
    user = User.query.filter(User.id == user_id).first()
    role = Role.query.filter(Role.name == "testing").first()
    #user_datastore.remove_role_from_user(user, 'testing')
    #user_datastore.create_role(name=new_role)
    user_datastore.remove_role(role)
    user_datastore.commit()
    return render_template('admin/roles.html', user=user)

@app.route("/admin/users")
@auth_required()
@roles_accepted('superadmin', 'admin')
def admin_users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)