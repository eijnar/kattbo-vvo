from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import DataRequired


class EditUserForm(FlaskForm):
    user_id = IntegerField('User ID', validators=[DataRequired()])
    hunt_team_id = IntegerField('User ID', validators=[DataRequired()])
    hunt_year_id = IntegerField('User ID', validators=[DataRequired()])
    