from app import db
from .tracking_mixin import TrackingMixin


class NotificationType(db.Model, TrackingMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    # Relationships
    tags = db.relationship('Tag', secondary='tags_notifications',
                           back_populates='allowed_notification_types')