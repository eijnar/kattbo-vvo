from flask import Blueprint, render_template, request, flash
from app import db
from app.tags.models import Tags

tags = Blueprint('tags', __name__, template_folder='templates')

@tags.route("/tags", methods=['GET', 'POST'])
def tags_admin():
    tags = Tags.query.all()
    return render_template("tags/tags_admin.html.j2", tags=tags)

@tags.route("/tags/<int:id>/delete", methods=['POST'])
def delete_tag(id):
    tag = Tags.query.get_or_404(id)
    db.session.delete(tag)
    db.session.commit()
    flash('Tagit bort {{ tag.name }}', 'success')
    return redirect(request.referrer)