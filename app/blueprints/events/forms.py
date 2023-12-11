from flask_wtf import FlaskForm
from wtforms import widgets
from wtforms.fields import StringField, SubmitField, TextAreaField, SelectMultipleField, SelectField, TimeField, BooleanField
from wtforms.widgets import TimeInput, TelInput
from wtforms.validators import DataRequired, Length, Optional

class EventForm(FlaskForm):
    event_type = SelectField('Event Type', validators=[DataRequired()], coerce=int)
    dates = StringField('Dates', validators=[DataRequired()])
    start_time = TimeField('Start', widget=TimeInput())
    end_time = StringField('End', widget=TelInput())
    joint_gathering = BooleanField('Gemensam samling', default=True)
    joint_gathering_place = SelectField('Samlingsplats', validators=[Optional()], coerce=int)
    hemmalaget_gathering_place = SelectField('Hemmalaget', validators=[Optional()], coerce=int)
    bortalaget_gathering_place = SelectField('Bortalaget', validators=[Optional()], coerce=int)
    submit = SubmitField('Create Event')

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class RegisterEventDayForm(FlaskForm):
    event_days = MultiCheckboxField('Event Days', coerce=int)
    submit = SubmitField('Anmäl')   