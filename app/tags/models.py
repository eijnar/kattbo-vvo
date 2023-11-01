from app import db
from flask_security.models import fsqla_v3 as fsqla
from app.mixins import TrackingMixin

class Tags(db.Model, TrackingMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    allow_sms = db.Column(db.Boolean, default=True)
    allow_email = db.Column(db.Boolean, default=True)

    events = db.relationship('Event', secondary='event_tags', back_populates='tags')
    users = db.relationship('User', secondary='user_tags', back_populates='tags')