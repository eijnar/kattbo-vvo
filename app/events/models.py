from app import db
from app.utils.mixins import TrackingMixin
from app.utils.crud import CRUDMixin


class Event(db.Model, TrackingMixin, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=True)

    # ForeignKeys
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_type_id = db.Column(db.Integer, db.ForeignKey('event_type.id'))
    event_type = db.relationship('EventType', back_populates='events')

    # Relationships
    event_days = db.relationship(
        'EventDay', back_populates='event', cascade='all,delete')


class EventDay(db.Model, TrackingMixin):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, default='07:00:00', nullable=True)
    cancelled = db.Column(db.SmallInteger, default=0)

    # ForeignKeys
    event_id = db.Column(db.Integer, db.ForeignKey(
        'event.id', ondelete='CASCADE'), nullable=False)

    # Relationships
    event = db.relationship('Event', back_populates='event_days')
    users_events = db.relationship('UsersEvents', back_populates='days')

    @property
    def is_active(self):
        active_days = EventDay.query.filter_by(
            event_id=self.id, cancelled=0).count()
        return active_days > 0


class EventType(db.Model, TrackingMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    # Relationships
    event_category_id = db.Column(db.Integer, db.ForeignKey('event_category.id'), nullable=False)
    events = db.relationship('Event', back_populates='event_type')
    tags = db.relationship(
        'Tag', secondary='event_type_tags', back_populates='event_types')


class EventCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    event_types = db.relationship('EventType', backref='event_category', lazy=True)

# Many to many


class UsersEvents(db.Model, TrackingMixin):
    id = db.Column(db.Integer, primary_key=True)

    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)
    day_id = db.Column(db.Integer, db.ForeignKey(
        'event_day.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', back_populates='users_events')
    days = db.relationship('EventDay', back_populates='users_events')


class EventTypeTags(db.Model, TrackingMixin):
    event_id = db.Column(db.Integer, db.ForeignKey(
        'event_type.id', ondelete='CASCADE'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey(
        'tag.id', ondelete='CASCADE'), primary_key=True)
