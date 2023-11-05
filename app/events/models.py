from app import db
from app.utils.mixins import TrackingMixin
from app.tags.models import Tags
from app.utils.crud import CRUDMixin

class Event(db.Model, TrackingMixin, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    event_type = db.Column(db.String(100), nullable=False)

    # Relationships
    days = db.relationship('EventDay', back_populates='event')
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tags = db.relationship('Tags', secondary='event_tags', back_populates='events')

    @classmethod
    def list_all(cls):
        return cls.get_all()

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
    
    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    day_id = db.Column(db.Integer, db.ForeignKey('event_day.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', back_populates='user_events')
    day = db.relationship('EventDay', back_populates='user_events')

class EventTags(db.Model, TrackingMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Relationships
    event_id = db.Column(db.Integer, db.ForeignKey('event.id', ondelete='CASCADE'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
