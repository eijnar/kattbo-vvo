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