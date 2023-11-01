from app import db
from flask_security.models import fsqla_v3 as fsqla
from app.event.models import UserEvent, EventDay
from app.mixins import TrackingMixin


roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id', ondelete='CASCADE')),
    extend_existing=True
)

class User(db.Model, fsqla.FsUserMixin):
    # Extra fields from the default FsUserMixin
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    phone_number = db.Column(db.String(12))

    # Relationships
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    subjects = db.relationship('UserSubject', back_populates='user')
    user_events = db.relationship('UserEvent', back_populates='user')
    created_events = db.relationship('Event', backref='creator', lazy='dynamic')

    def __repr__(self):
        return str(self.__dict__)

class Role(db.Model, fsqla.FsRoleMixin):
    # Use the built in functions for now
    def __repr__(self):
        return str(self.__dict__)

class Subject(db.Model, TrackingMixin):
    __tablename__ = 'subject'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.Text)

    # Relationships
    user_subjects = db.relationship('UserSubject', back_populates='subject')

    def __repr__(self):
        return str(self.__dict__)
    
class UserSubject(db.Model, TrackingMixin):
    __tablename__ = 'user_subject'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id', ondelete='CASCADE'), primary_key=True)
    opt_in_email = db.Column(db.Boolean, default=False)
    opt_in_sms = db.Column(db.Boolean, default=False)

    # Relationships
    user = db.relationship('User', back_populates='subjects')
    subject = db.relationship('Subject', back_populates='user_subjects')

    def __repr__(self):
        return str(self.__dict__)