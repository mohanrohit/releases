# new_application_form.py

from flask.ext.wtf import Form

from wtforms import StringField
from wtforms.validators import DataRequired

class NewApplicationForm(Form):
    name = StringField("name", validators=[DataRequired()])
    version = StringField("version", validators=[DataRequired()])