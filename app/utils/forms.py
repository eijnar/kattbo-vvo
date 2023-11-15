from flask_security import RegisterForm
from wtforms import StringField
from wtforms.validators import DataRequired

class ExtendedRegisterForm(RegisterForm):
    first_name = StringField('Förnamn', [DataRequired()])
    last_name = StringField('Efternamn', [DataRequired()])
    phone_number = StringField('Telefonnummer', [DataRequired()])