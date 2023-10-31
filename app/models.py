from app import db, ma
from flask_security.models import fsqla_v3 as fsqla

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
    extend_existing=True
)

class User(db.Model, fsqla.FsUserMixin):
    __tablename__ = 'user'
    # ID setup and active
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False)
    active = db.Column(db.Boolean())
    # User information
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    phone_number = db.Column(db.String(12))
    # Tracking information
    confirmed_at = db.Column(db.DateTime())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(64))
    current_login_ip = db.Column(db.String(64))
    login_count = db.Column(db.Integer)
    # Relationships
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    subjects = db.relationship('UserSubject', back_populates='user')

    def __repr__(self):
        return str(self.__dict__)

class Role(db.Model, fsqla.FsRoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(255))
    permissions = db.Column(db.Text)
    update_datetime = db.Column(db.DateTime(), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return str(self.__dict__)

class Subject(db.Model):
    __tablename__ = 'subject'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.Text)
    user_subjects = db.relationship('UserSubject', back_populates='subject')

    def __repr__(self):
        return str(self.__dict__)
    
class UserSubject(db.Model):
    __tablename__ = 'user_subject'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), primary_key=True)
    opt_in_email = db.Column(db.Boolean, default=False)
    opt_in_sms = db.Column(db.Boolean, default=False)
    user = db.relationship('User', back_populates='subjects')
    subject = db.relationship('Subject', back_populates='user_subjects')

    def __repr__(self):
        return str(self.__dict__)

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ("id", "first_name", "last_name", "email", "phone_number")
        model = User
        load_instance = True