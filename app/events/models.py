from app import db
from flask_security.models import fsqla_v3 as fsqla
from app.mixins import TrackingMixin
from app.tags.models import Tags

class Event(db.Model, TrackingMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)

    # Relationships
    days = db.relationship('EventDay', back_populates='event')
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tags = db.relationship('Tags', secondary='event_tags', back_populates='events')

class EventDay(db.Model, TrackingMixin):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id', ondelete='CASCADE'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, default='07:00:00', nullable=True)

    # Relationships
    event = db.relationship('Event', back_populates='days')
    user_events = db.relationship('UserEvent', back_populates='day')

class UserEvent(db.Model, TrackingMixin):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    accepted_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    day_id = db.Column(db.Integer, db.ForeignKey('event_day.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', back_populates='user_events')
    day = db.relationship('EventDay', back_populates='user_events')

class EventTags(db.Model, TrackingMixin):
    id = db.Column(db.Integer, primary_key=True)

    # Relationships
    event_id = db.Column(db.Integer, db.ForeignKey('event.id', ondelete='CASCADE'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
