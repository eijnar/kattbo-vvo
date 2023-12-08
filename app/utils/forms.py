from flask import request
from flask_wtf import FlaskForm
from flask_security import RegisterForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class ExtendedRegisterForm(RegisterForm):
    first_name = StringField('Förnamn', [DataRequired()])
    last_name = StringField('Efternamn', [DataRequired()])
    phone_number = StringField('Telefonnummer', [DataRequired()])

class NotificationForm(FlaskForm):
    message = TextAreaField('Meddelande', validators=[DataRequired()])
    submit = SubmitField('Skicka')


class SearchForm(FlaskForm):
    q = StringField(
        'Search',
        validators=[DataRequired()],
        render_kw={'placeholder': 'Search ...'})

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'meta' not in kwargs:
            kwargs['meta'] = {'csrf': False}
        super(SearchForm, self).__init__(*args, **kwargs)