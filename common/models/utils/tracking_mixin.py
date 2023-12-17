from app import db


class TrackingMixin:
    """Adds tracking information to a model by including created_at and updated_at fields.

    Attributes:
        created_at (db.Column): A field of type TIMESTAMP that stores the timestamp of when the model instance was created.
            It has a default value of the current timestamp and is not nullable.
        updated_at (db.Column): A field of type TIMESTAMP that stores the timestamp of when the model instance was last updated.
            It has a default value of the current timestamp and is not nullable.
    """

    created_at = db.Column(
        db.TIMESTAMP(), server_default=db.func.current_timestamp(), nullable=False)
    updated_at = db.Column(
        db.TIMESTAMP(), server_default=db.func.current_timestamp(), nullable=False)
