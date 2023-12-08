from flask_wtf import FlaskForm
from wtforms.fields import StringField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    title = StringField('Titel', validators=[DataRequired()])
    content = TextAreaField(validators=DataRequired())
    tags = SelectMultipleField('Taggar')