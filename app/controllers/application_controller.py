# ApplicationController

from flask import render_template
from flask import url_for
from flask import redirect

from base_controller import *

from app.forms import NewApplicationForm
from app.forms import UndefinedApplicationForm

import re
import string

def name_to_id(application_name):
    # lowercase the application name, and replace any whitespace with
    # hyphens
    return re.sub(r"\W+", "-", application_name.lower())

def id_to_name(application_id):
    # separate the parts of the id split by hyphens and capitalize
    # each part
    return " ".join(map(string.capitalize, application_id.split("-")))

def create_application(application_name):
    application_id = name_to_id(application_name)

    application = Application(id=application_id, name=application_name)
    application.save()

    return application


class ApplicationController(BaseController):
    def __init__(self):
        BaseController.__init__(self)

    @route("/applications")
    def index(self):
        applications = Application.query.all()

        return render_template("applications/index.html", applications=applications)

    @route("/applications/<id>") # id is a string, the name of the application, lowercased
    def get(self, id):
        application = Application.query.filter(Application.id == id).first()
        if not application:
            return redirect(url_for("ApplicationController:undefined", id=id))

        versions = application.versions

        return render_template("applications/get.html", id=id, application=application, versions=versions)

    @route("/applications/undefined", methods=["GET", "POST"])
    def undefined(self):
        application_id = request.values.get("id") or ""
        application_name = id_to_name(application_id)

        undefined_application_form = UndefinedApplicationForm(request.values)

        if undefined_application_form.validate_on_submit():

            if undefined_application_form.yes.data:
                create_application(application_name)

                return redirect(url_for("ApplicationController:get", id=name_to_id(application_name)))

            if undefined_application_form.no.data:
                return redirect(url_for("ApplicationController:index"))

        return render_template("applications/undefined_application.html",
            id=application_id,
            name=application_name,
            form=undefined_application_form
        )

    @route("/applications/new", methods=["GET", "POST"])
    def new(self):
        new_application_form = NewApplicationForm(request.values)

        if new_application_form.validate_on_submit():
            application_name = self.params["name"]
            application_id = name_to_id(application_name)

            if not Application.exists(application_id):
                create_application(application_id)

            return redirect(url_for("ApplicationController:get", id=application_id))

        return render_template("applications/new.html", form=new_application_form)
