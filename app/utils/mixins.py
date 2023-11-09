from app import db
from sqlalchemy import text
from flask_security.models import fsqla_v3 as fsqla


class TrackingMixin:
    """Adds tracking information
    
    adds created_at and updated_at to the model
    """
    
    created_at = db.Column(db.TIMESTAMP(), server_default=db.func.current_timestamp(), nullable=False)
    updated_at = db.Column(db.TIMESTAMP(), server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), nullable=False)