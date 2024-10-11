from app import db
from .tracking_mixin import TrackingMixin


class Document(db.Model, TrackingMixin):
    id = db.Column(db.Integer, primary_key=True)
    short_name = db.Column(db.String(50), nullable=False, unique=True)
    document = db.Column(db.Text)