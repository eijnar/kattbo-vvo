from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired


class EditUserForm(FlaskForm):
    user_id = IntegerField('User ID', validators=[DataRequired()])
    hunt_team_id = IntegerField('HuntTeam ID', validators=[DataRequired()])
    hunt_year_id = IntegerField('HuntYear ID', validators=[DataRequired()])
    stand_number = StringField('Stand number', validators=[DataRequired()])
    