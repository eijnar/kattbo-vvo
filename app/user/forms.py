from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Email, EqualTo
from wtforms.meta import DefaultMeta


class UpdateProfileForm(FlaskForm):
    first_name = StringField('Förnamn', validators=[InputRequired(message="Du måste fylla i detta!")])
    last_name = StringField('Efternamn')
    email = StringField('E-post', validators=[InputRequired(message="Du måste fylla i detta!"), Email()])
    phone_number = StringField('Mobilnummer')
    submit = SubmitField('Uppdatera profil')

def OptInFormMeta(subjects):
    class Meta(DefaultMeta):
        pass

    attrs = {
        'submit': SubmitField('Save'),
        'Meta': Meta,
    }

    for subject in subjects:
        attrs['subject_email_' + str(subject.id)] = BooleanField(subject.name + ' Email')
        attrs['subject_sms_' + str(subject.id)] = BooleanField(subject.name + ' SMS')

    return type('OptInForm', (FlaskForm,), attrs)