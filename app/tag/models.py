from app import db
from app.utils.mixins import TrackingMixin

class Tag(db.Model, TrackingMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(50), nullable=False, unique=True)

    # Relationships
    tag_users = db.relationship('User', secondary='users_tags', back_populates='tags')
    tag_category = db.relationship('TagCategory', secondary='tags_categories', back_populates='tags')
    allowed_roles = db.relationship('Role', secondary='roles_tags', back_populates='allowed_tags')
    allowed_notification_types = db.relationship('NotificationType', secondary='tags_notifications', back_populates='tags')

class TagCategory(db.Model, TrackingMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.Text)

    # Relationships
    tags = db.relationship('Tag', secondary='tags_categories', back_populates='tag_category')
    events = db.relationship('Event', backref='tag_category')

class TagsCategories(db.Model, TrackingMixin):
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id', ondelete='CASCADE'), primary_key=True)
    tag_category_id = db.Column(db.Integer, db.ForeignKey('tag_category.id', ondelete='CASCADE'), primary_key=True)
    