from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField


class AddGeopointForm(FlaskForm):
    name = StringField('Namn')
    lat = StringField('Latitude')
    long = StringField('Longitude')
    category = StringField('Kategori')
    description = StringField('Beskrivning')
    submit = SubmitField('Skapa punkt')
