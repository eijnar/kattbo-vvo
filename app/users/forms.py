from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Email, DataRequired


class UpdateProfileForm(FlaskForm):
    first_name = StringField('Förnamn', validators=[InputRequired(message="Du måste fylla i detta!")])
    last_name = StringField('Efternamn')
    email = StringField('E-post', validators=[InputRequired(message="Du måste fylla i detta!"), Email()])
    phone_number = StringField('Mobilnummer')
    submit = SubmitField('Uppdatera')

def UserPreferenceFormFactory(notification_options, user_preferences):
    """
    Factory function to create a FlaskForm class dynamically based on notification options.
    """
    # Create a dictionary to hold the form fields
    form_attrs = {}

    # Dynamically add a BooleanField for each notification type in each tag category
    for tag_category, notification_types in notification_options.items():
        for notification_type in notification_types:
            field_name = f'notification_{tag_category.id}_{notification_type.id}'  # Use ID to ensure uniqueness
            default_value = user_preferences.get((tag_category.id, notification_type.id))
            form_attrs[field_name] = BooleanField(notification_type.name, default=default_value)

    # Add a submit field to the form attributes
    form_attrs['submit'] = SubmitField('Update Preferences')

    # Create the form class with a new type
    return type('UserPreferenceForm', (FlaskForm,), form_attrs)