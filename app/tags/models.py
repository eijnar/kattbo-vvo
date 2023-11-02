from app import db
from sqlalchemy.sql import expression
from app.utils.mixins import TrackingMixin
from app.utils.crud import CRUDMixin

class Tags(db.Model, TrackingMixin, CRUDMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    allow_sms = db.Column(db.Boolean, server_default=expression.true(), nullable=False)
    allow_email = db.Column(db.Boolean,server_default=expression.true(), nullable=False)

    # Relationships
    events = db.relationship('Event', secondary='event_tags', back_populates='tags')
    users = db.relationship('User', secondary='user_tags', back_populates='tags')

    @classmethod
    def list_all(cls):
        return cls.get_all()