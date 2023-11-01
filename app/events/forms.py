from flask_wtf import FlaskForm
from wtforms.fields import DateField, StringField, SubmitField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired

class EventForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    dates = StringField('Dates', validators=[DataRequired()])
    submit = SubmitField('Skapa')

class AcceptEventForm(FlaskForm):
    days = SelectMultipleField('Days', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Anmäl')