from flask_wtf import FlaskForm
from wtforms import widgets
from wtforms.fields import StringField, SubmitField, TextAreaField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, Length

class EventForm(FlaskForm):
    tag_category = SelectField('Event Type', validators=[DataRequired()], coerce=int)
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=2, max=500)])
    dates = StringField('Dates', validators=[DataRequired()])
    submit = SubmitField('Create Event')

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class RegisterEventDayForm(FlaskForm):
    event_days = MultiCheckboxField('Event Days', coerce=int)
    submit = SubmitField('Anmäl')