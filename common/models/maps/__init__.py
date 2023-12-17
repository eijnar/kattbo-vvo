from app import db
from geoalchemy2 import Geometry
from models.utils.tracking_mixin import TrackingMixin

class PointOfIntrest(db.Model, TrackingMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=True)
    geopoint = db.Column(Geometry('POINT'))

    