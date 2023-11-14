from app import db
from app.utils.mixins import TrackingMixin
from app.users.models import User


class HuntYear(db.Model, TrackingMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)


class HuntTeam(db.Model, TrackingMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)


# New model to link User, HuntTeam, and HuntYear
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