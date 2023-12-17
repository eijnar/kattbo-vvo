from app import db
from .tracking_mixin import TrackingMixin


class ShortLink(db.Model, TrackingMixin):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(2048), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=True)