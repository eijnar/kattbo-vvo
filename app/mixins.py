from app import db
from flask_security.models import fsqla_v3 as fsqla


class TrackingMixin:
    """Adds tracking information
    
    adds created_at and updated_at to the model
    """
    
    created_at = db.Column(db.DateTime(), default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime(), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())