from app import db
from flask_security.models import fsqla_v3 as fsqla
from app.tags.models import Tags
from app.events.models import UserEvent, EventDay
from app.utils.mixins import TrackingMixin
from app.utils.crud import CRUDMixin


roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id', ondelete='CASCADE')),
    extend_existing=True
)

class User(db.Model, fsqla.FsUserMixin, CRUDMixin):
    # Extra fields from the default FsUserMixin
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    phone_number = db.Column(db.String(12))

    # Relationships
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    user_events = db.relationship('UserEvent', back_populates='user')
    created_events = db.relationship('Event', backref='creator', lazy='dynamic')
    tags = db.relationship('Tags', secondary='user_tags', back_populates='users')

    @classmethod
    def list_all(cls):
        return cls.get_all()

class Role(db.Model, fsqla.FsRoleMixin):
    # Use the built in functions for now
    def __repr__(self):
        return str(self.__dict__)


class UserTags(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subscribe_sms = db.Column(db.Boolean, default=False)
    subscribe_email = db.Column(db.Boolean, default=False)

    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)