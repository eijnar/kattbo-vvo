from app import db
from app.utils.mixins import TrackingMixin
from geoalchemy2 import Geometry
from datetime import datetime


class HuntYear(db.Model, TrackingMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    stand_assignments = db.relationship('StandAssignment', backref='hunt_year', lazy=True)
    animal_quotas = db.relationship('AnimalQuota', back_populates='hunt_year')


class HuntTeam(db.Model, TrackingMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    
    # Relationships
    areas = db.relationship('Area', back_populates='hunt_team', lazy=True)
    animal_quotas = db.relationship('AnimalQuota', back_populates='hunt_team')


class UserTeamYear(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    hunt_team_id = db.Column(db.Integer, db.ForeignKey('hunt_team.id'), nullable=False)
    hunt_year_id = db.Column(db.Integer, db.ForeignKey('hunt_year.id'), nullable=False)
    hunt_team = db.relationship('HuntTeam')
    hunt_year = db.relationship('HuntYear')
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'hunt_year_id', name='unique_user_per_year'),
    )


class Area(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    boundary = db.Column(Geometry('POLYGON'))

    hunt_team_id = db.Column(db.Integer, db.ForeignKey('hunt_team.id'))

    # Relationships
    stands = db.relationship('Stand', backref='area', lazy=True)

    hunt_team = db.relationship('HuntTeam', back_populates='areas')

class Stand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    geopoint = db.Column(Geometry('POINT'))

    # Relationships
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('number', 'area_id', name='_stand_number_area_uc'),
    )


class StandAssignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stand_id = db.Column(db.Integer, db.ForeignKey('stand.id'), nullable=False)
    hunt_year_id = db.Column(db.Integer, db.ForeignKey('hunt_year.id'), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'stand_id', 'hunt_year_id', name='_user_stand_year_uc'),
    )


class AnimalQuota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hunt_year_id = db.Column(db.Integer, db.ForeignKey('hunt_year.id'), nullable=False)
    hunt_year = db.relationship('HuntYear', back_populates='animal_quotas')
    animal_type_id = db.Column(db.Integer, db.ForeignKey('animal_type.id'), nullable=False)
    animal_type = db.relationship('AnimalType', back_populates='quotas')
    initial_quota = db.Column(db.Integer, nullable=True)
    animals_shot = db.relationship('AnimalShot', back_populates='quota')
    hunt_team_id = db.Column(db.Integer, db.ForeignKey('hunt_team.id'), nullable=False)
    hunt_team = db.relationship('HuntTeam', back_populates='animal_quotas')


class AnimalType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    quotas = db.relationship('AnimalQuota', back_populates='animal_type')
    group = db.Column(db.String(100), nullable=False)


class AnimalShot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_shot = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    weight = db.Column(db.Float)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20), nullable=False)
    animal_type_id = db.Column(db.Integer, db.ForeignKey('animal_type.id'))
    animal_type = db.relationship('AnimalType')
    antler_type = db.Column(db.String(255))
    antlers = db.Column(db.String(255))  # Could be an enum if you have specific categories
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User')
    quota_id = db.Column(db.Integer, db.ForeignKey('animal_quota.id'), nullable=False)
    quota = db.relationship('AnimalQuota', back_populates='animals_shot')