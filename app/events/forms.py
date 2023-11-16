from flask_wtf import FlaskForm
from wtforms import widgets
from wtforms.fields import StringField, SubmitField, TextAreaField, SelectMultipleField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Length

class EventForm(FlaskForm):
    event_type = SelectField('Event Type', validators=[DataRequired()], coerce=int)
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=2, max=255)])
    dates = StringField('Dates', validators=[DataRequired()])
    time = StringField('Time')
    submit = SubmitField('Create Event')

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class RegisterEventDayForm(FlaskForm):
    event_days = MultiCheckboxField('Event Days', coerce=int)
    submit = SubmitField('Anmäl')