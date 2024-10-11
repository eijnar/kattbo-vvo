from app import db


class NotificationTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    celery_task_id = db.Column(db.String, nullable=False)

    # Relationships
    event_type = db.Column(db.Integer, db.ForeignKey(
        'event_type.id', ondelete='CASCADE'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey(
        'event.id', ondelete='CASCADE'), nullable=False)
