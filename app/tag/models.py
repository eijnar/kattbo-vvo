from app import db
from sqlalchemy.sql import expression
from app.utils.mixins import TrackingMixin

class Tag(db.Model, TrackingMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=True)
    allow_sms = db.Column(db.Boolean, server_default=expression.true())
    allow_email = db.Column(db.Boolean, server_default=expression.true())

    # Relationships
    users = db.relationship('User', secondary='users_tags', back_populates='tags')
    category = db.relationship('TagCategory', secondary='tags_categories', back_populates='tags')

class TagCategory(db.Model, TrackingMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)


    # Relationships
    events = db.relationship('Event', secondary='events_tags', back_populates='tag_category')
    tags = db.relationship('Tag', secondary='tags_categories', back_populates='category')

class TagsCategories(db.Model, TrackingMixin):
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id', ondelete='CASCADE'), primary_key=True)
    tag_category_id = db.Column(db.Integer, db.ForeignKey('tag_category.id', ondelete='CASCADE'), primary_key=True)
    