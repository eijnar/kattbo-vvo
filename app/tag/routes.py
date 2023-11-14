from flask import Blueprint, render_template, request, flash
from flask_security import auth_required, roles_accepted
from app import db
from app.tag.models import Tag, TagCategory

tags = Blueprint('tags', __name__, template_folder='templates')


@tags.route("/tags", methods=['GET', 'POST'])
@auth_required
@roles_accepted('admin')
def tags_admin():
    tags = Tag.query.all()
    categories = TagCategory.query.all()
    return render_template("tags/tags_admin.html.j2", tags=tags, categories=categories)


@tags.route("/tags/<int:id>/delete", methods=['POST'])
@auth_required
@roles_accepted('admin')
def delete_tag(id):
    tags = Tag.query.get_or_404(id)
    db.session.delete(tag)
    db.session.commit()
    flash('Tagit bort {{ tag.name }}', 'success')
    return redirect(request.referrer)
