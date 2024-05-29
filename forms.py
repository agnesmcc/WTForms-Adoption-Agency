from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class PetForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    species = StringField('Species', validators=[DataRequired()])
    photo_url = StringField('Photo URL')
    age = StringField('Age')
    notes = StringField('Notes')
