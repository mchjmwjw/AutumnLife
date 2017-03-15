from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import Required

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('submit')

