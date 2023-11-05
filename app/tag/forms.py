from flask_wtf import FlaskForm
from wtforms import widgets
from wtforms.fields import StringField, SubmitField, BooleanField, SelectMultipleField
from wtforms.validators import DataRequired, Length

class TagForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    category = SelectField('Kategori', validators=[DataRequired()], coerce=int)
    description = StringField('Beskrivning', nullable=True)
    submit = SubmitField()

class TagCategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    allow_sms = BooleanField('Tillåt SMS utskick')
    allow_email = BooleanField('Tillåt E-post utskick')
    tags = SelectMultipleField('Tag', coerce=int)
    submit = SubmitField()