from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Email, EqualTo
from wtforms.meta import DefaultMeta


class UpdateProfileForm(FlaskForm):
    first_name = StringField('Förnamn', validators=[InputRequired(message="Du måste fylla i detta!")])
    last_name = StringField('Efternamn')
    email = StringField('E-post', validators=[InputRequired(message="Du måste fylla i detta!"), Email()])
    phone_number = StringField('Mobilnummer')
    submit = SubmitField('Uppdatera')

def OptInFormMeta(tags):
    class Meta(DefaultMeta):
        pass

    attrs = {
        'submit': SubmitField('Uppdatera'),
        'Meta': Meta,
    }

    for tag in tags:
        attrs['tag_email_' + str(tag.id)] = BooleanField(tag.name + ' Email')
        attrs['tag_sms_' + str(tag.id)] = BooleanField(tag.name + ' SMS')
    return type('OptInForm', (FlaskForm,), attrs)