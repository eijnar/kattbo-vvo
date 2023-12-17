from app import db


class TagsNotifications(db.Model):
    __table_args__ = {'extend_existing': True}
    tag_id = db.Column('tag_id', db.Integer,
                       db.ForeignKey('tag.id'), primary_key=True)
    notification_type_id = db.Column('notification_type_id', db.Integer, db.ForeignKey(
        'notification_type.id'), primary_key=True)