from flask_wtf import FlaskForm
from wtforms import widgets
from wtforms.fields import StringField, SubmitField, TextAreaField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, Length

#class EventForm(FlaskForm):
#    name = StringField('Name', validators=[DataRequired()])
#    description = TextAreaField('Description', validators=[DataRequired()])
#    
#    submit = SubmitField('Skapa')

class EventForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    event_type = SelectField('Event Type', validators=[DataRequired()], choices=[('conference', 'Conference'), ('seminar', 'Seminar'), ('workshop', 'Workshop')])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=2, max=500)])
    tags = SelectMultipleField('Tags', coerce=int)  # Define tags field as a multi-select field with integer values
    dates = StringField('Dates', validators=[DataRequired()])
    submit = SubmitField('Create Event')

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class RegisterEventDayForm(FlaskForm):
    event_days = MultiCheckboxField('Event Days', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Register')