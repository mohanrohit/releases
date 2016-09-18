# new_application_form.py

from flask.ext.wtf import Form

from wtforms import StringField

from wtforms.validators import InputRequired
from wtforms.validators import Regexp

class NewApplicationForm(Form):
    name = StringField("name",
        validators=[
            InputRequired(message="The application name is required.")
        ]
    )
