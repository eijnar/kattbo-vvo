from app import db
from app.utils.mixins import TrackingMixin

# Notification models 
class TagsNotifications(db.Model):
    __table_args__ = {'extend_existing': True}
    tag_id = db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
    notification_type_id = db.Column('notification_type_id', db.Integer, db.ForeignKey('notification_type.id'), primary_key=True)

class NotificationType(db.Model, TrackingMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    # Relationships
    tags = db.relationship('Tag', secondary='tags_notifications', back_populates='allowed_notification_types')
 
# Shortlink models 
class ShortLink(db.Model, TrackingMixin):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(2048), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=True)

# Documents model
class Document(db.Model, TrackingMixin):
    id = db.Column(db.Integer, primary_key=True)
    short_name = db.Column(db.String(50), nullable=False, unique=True)
    document = db.Column(db.Text)