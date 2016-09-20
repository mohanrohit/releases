# ApplicationController

from flask import render_template
from flask import url_for
from flask import redirect
from flask import abort

from base_controller import *

from app.forms import NewApplicationForm
from app.forms import UndefinedApplicationForm

import re
import string

def name_to_slug(application_name):
    # lowercase the application name, and replace any whitespace with
    # hyphens
    return re.sub(r"\W+", "-", application_name.lower())

def slug_to_name(application_slug):
    # separate the parts of the slug split by hyphens and capitalize
    # each part
    return " ".join(map(string.capitalize, application_slug.split("-")))

def create_application(application_name):
    application_slug = name_to_slug(application_name)

    application = Application(slug=application_slug, name=application_name)
    application.save()

    return application


class ApplicationController(BaseController):
    def __init__(self):
        BaseController.__init__(self)

    @route("")
    def index(self):
        applications = Application.query.all()

        return render_template("applications/index.html", applications=applications)

    @route("/<slug>") # slug is a string -- the lowercased name of the application
    def get(self, slug):
        application = Application.get_by_slug(slug)
        if not application:
            return redirect(url_for("ApplicationController:undefined", slug=slug))

        versions = application.versions

        return render_template("applications/get.html", slug=slug, application=application, versions=versions)

    @route("/undefined", methods=["GET", "POST"])
    def undefined(self):
        application_slug = request.values.get("slug") or ""
        if not application_slug:
            abort(404) # another more pertinent error

        application_name = slug_to_name(application_slug)

        undefined_application_form = UndefinedApplicationForm(request.values)

        if undefined_application_form.validate_on_submit():
            if undefined_application_form.yes.data:
                create_application(application_name)

                return redirect(url_for("ApplicationController:get", slug=application_slug))

            if undefined_application_form.no.data:
                return redirect(url_for("ApplicationController:index"))

        return render_template("applications/undefined_application.html",
            slug=application_slug,
            name=application_name,
            form=undefined_application_form
        )

    @route("/new", methods=["GET", "POST"])
    def new(self):
        new_application_form = NewApplicationForm(request.values)

        if new_application_form.validate_on_submit():
            application_name = self.params["name"]
            application_slug = name_to_slug(application_name)

            if not Application.get_by_slug(application_slug):
                create_application(application_name)

            return redirect(url_for("ApplicationController:get", slug=application_slug))

        return render_template("applications/new.html", form=new_application_form)
