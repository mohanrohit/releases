# new_application_form.py

from flask.ext.wtf import Form

from wtforms import HiddenField
from wtforms import StringField
from wtforms import SubmitField

class UndefinedApplicationForm(Form):
    #id = HiddenField("id")
    id = StringField("id")
    yes = SubmitField(label="Yes")
    no = SubmitField(label="No")
