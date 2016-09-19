# ApplicationController

from flask import render_template
from flask import url_for
from flask import redirect

from base_controller import *

from app.forms import NewApplicationForm
from app.forms import UndefinedApplicationForm

import re
import string

class ApplicationController(BaseController):
    def __init__(self):
        BaseController.__init__(self)

    @staticmethod
    def name_to_id(application_name):
        # lowercase the application name, and replace any whitespace with
        # hyphens
        return re.sub(r"\W+", "-", application_name.lower())

    @staticmethod
    def id_to_name(application_id):
        # separate the parts of the id split by hyphens and capitalize
        # each part
        return " ".join(map(string.capitalize, application_id.split("-")))

    @staticmethod
    def create_application(application_id, application_name):
        application = Application(id=application_id, name=application_name)
        application.save()

        return application

    @route("/applications")
    def index(self):
        applications = Application.query.all()

        return render_template("applications/index.html", applications=applications)

    # @route("/applications/<application_name>")
    # def get(self, application_name):
        # application = Application.query.filter(Application.name == application_name).first()
        # if not application:
            # return render_template("applications/not_found.html", name=application_name)

        # versions = application.versions

        # return render_template("applications/get.html", application=application, versions=versions)

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

        undefined_application_form = UndefinedApplicationForm(request.values)
        if undefined_application_form.validate_on_submit():
            print "valid on submit"
            if undefined_application_form.yes.data:
                print "yes pressed"
                ApplicationController.create_application(application_id)

                return redirect(url_for("ApplicationController:get", id=application_id))

            if undefined_application_form.no.data:
                print "no pressed"
                return redirect(url_for("ApplicationController:index"))

        return render_template("applications/undefined_application.html", id=application_id, name=ApplicationController.id_to_name(application_id), form=undefined_application_form)

    @route("/applications/new", methods=["GET", "POST"])
    def new(self):
        new_application_form = NewApplicationForm(request.values)
        
        if new_application_form.validate_on_submit():
            create_application(self.params["id"], self.params["name"])

            return redirect(url_for("ApplicationController:get", id=self.params["id"]))

        return render_template("applications/new.html", form=new_application_form)
