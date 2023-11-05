from app import db
from app.utils.mixins import TrackingMixin
from app.utils.crud import CRUDMixin

class Event(db.Model, TrackingMixin, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    event_type = db.Column(db.String(100), nullable=False)

    # Relationships
    event_days = db.relationship('EventDay', back_populates='event')
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tag_category = db.relationship('TagCategory', secondary='events_tags', back_populates='events')

class EventDay(db.Model, TrackingMixin):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id', ondelete='CASCADE'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, default='07:00:00', nullable=True)

    # Relationships
    event = db.relationship('Event', back_populates='event_days')
    users_events = db.relationship('UsersEvents', back_populates='days')

class UsersEvents(db.Model, TrackingMixin):
    id = db.Column(db.Integer, primary_key=True)
    
    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    day_id = db.Column(db.Integer, db.ForeignKey('event_day.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', back_populates='users_events')
    days = db.relationship('EventDay', back_populates='users_events')

class EventsTags(db.Model, TrackingMixin):
    event_id = db.Column(db.Integer, db.ForeignKey('event.id', ondelete='CASCADE'), primary_key=True)
    tag_category_id = db.Column(db.Integer, db.ForeignKey('tag_category.id', ondelete='CASCADE'), primary_key=True)
