from flask_wtf import FlaskForm
from wtforms.fields import SelectField, DateField, StringField, SubmitField, RadioField, BooleanField
from wtforms.validators import DataRequired, Optional
from wtforms.widgets import DateInput
from datetime import datetime

class RegisterShotMoose(FlaskForm):
    moose_type = SelectField('Älgtyp', validators=[DataRequired()], coerce=int)
    date = DateField('Datum', validators=[DataRequired()], widget=DateInput(), default=datetime.today)
    weight = StringField('Vikt (KG)')
    age = StringField('Ålder')
    hunter = SelectField('Jägare', validators=[DataRequired()], coerce=int)
    gender = RadioField('Kön', choices=[("male", "Oxe"), ("female", "Kviga")], validators=[Optional()])
    antlers = StringField('Antal piggar', validators=[Optional()])
    antler_type = RadioField('Horntyp', choices=[("skovel", "Skovel"), ("stång", "Stång")], validators=[Optional()])
    milk = BooleanField('Mjölk', default=False, validators=[Optional()])
    submit = SubmitField('Registrera')