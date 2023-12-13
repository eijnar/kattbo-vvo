from app import db
from flask_security import UserMixin, RoleMixin
from flask_security.models import fsqla_v3 as fsqla 
from app.utils.mixins import TrackingMixin
from app.utils.crud import CRUDMixin

class RolesUsers(db.Model):
    __table_args__ = {'extend_existing': True}
    role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete='CASCADE'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)

class RolesTags(db.Model):
    __table_args__ = {'extend_existing': True}
    role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete='CASCADE'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id', ondelete='CASCADE'), primary_key=True)

class User(db.Model, fsqla.FsUserMixin, UserMixin, CRUDMixin):
    # Extra fields from the default FsUserMixin
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))
    profile_picture = db.Column(db.String(255))

    # Relationships
    roles = db.relationship('Role', secondary='roles_users', backref=db.backref('users', lazy='dynamic'))
    users_events = db.relationship('UsersEvents', back_populates='user')
    created_events = db.relationship('Event', backref='creator', lazy='dynamic')
    tags = db.relationship('Tag', secondary='users_tags', back_populates='tag_users')
    general_preferences = db.relationship('UserPreference', back_populates='preference_user')
    notification_preferences = db.relationship('UserNotificationPreference', back_populates='user_notification_preferences')
    hunt_years = db.relationship('UserTeamYear', backref='user', lazy='dynamic')
    stand_assignments = db.relationship('StandAssignment', backref='user', lazy='dynamic')
    posts = db.relationship('Post', backref='author', lazy=True)

    def set_opt_in(self, event_type_id, opt_in=True):
        # Loop through the user's notification preferences to find if one already exists
        notification_preference = None
        for preference in self.notification_preferences:
            if preference.event_type_id == event_type_id:
                notification_preference = preference
                break
        
        if notification_preference:
            # Update the existing preference
            notification_preference.opt_in = opt_in
        else:
            # Or create a new preference record
            notification_preference = UserNotificationPreference(user_id=self.id, event_type_id=event_type_id, opt_in=opt_in)
            db.session.add(notification_preference)

        # Commit changes to the database
        db.session.commit()

class UserNotificationPreference(db.Model, TrackingMixin):
    opt_in = db.Column(db.Boolean, default=True) 
    
    # ForeignKeys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    event_type_id = db.Column(db.Integer, db.ForeignKey('event_type.id'), primary_key=True)
    notification_type_id = db.Column(db.Integer, db.ForeignKey('notification_type.id'), primary_key=True)

    # Relationships
    user_notification_preferences = db.relationship('User', back_populates='notification_preferences')
    event_type = db.relationship('EventType')
    notification_type = db.relationship('NotificationType')

class Role(db.Model, fsqla.FsRoleMixin, RoleMixin):
    
    # Relationships
    allowed_tags = db.relationship('Tag', secondary='roles_tags', back_populates='allowed_roles')

class UserPreference(db.Model, TrackingMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Relationships
    preference_user = db.relationship('User', back_populates='general_preferences')

    def __repr__(self):
        return f'<UserPreference user_id={self.user_id} tag_category_id={self.tag_category_id} opt_in={self.opt_in}>'

class UsersTags(db.Model, TrackingMixin):
    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id', ondelete='CASCADE'), primary_key=True)
