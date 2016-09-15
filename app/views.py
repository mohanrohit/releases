from app import app

from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask import make_response
from flask import flash
from flask import get_flashed_messages

from flask.views import MethodView

import re
import datetime

applications = {
    "argo": { "name": "Argo" }
}

application_versions = {
    "argo": {
       "2.9.1": {}
    }
}

def application_exists(application_id):
    return application_id in applications

def version_exists(application_id, application_version):
    if not application_exists(application_id):
        return False

    return application_version in application_versions[application_id]

class ApplicationView(MethodView):
    def get(self):
        return render_template("new_application.html")

    def post(self):
        errors = []

        application_name = request.form["application_name"] or ""
        if application_name.strip() == "":
            errors.append("Please enter an application name.")

        application_name = re.sub(r"\s+", " ", application_name)

        application_version = request.form["application_version"] or ""

        application_id = application_name.lower().replace(" ", "-")
        if application_exists(application_id) and version_exists(application_id, application_version):
            errors.append("An application by that name already exists with the version you entered.")

        if application_version.strip() == "":
            errors.append("Please enter a version number in the <major.minor.patch> format")

        if errors:
            return render_template("new_application.html", **locals())

        if not application_exists(application_id):
            applications[application_id] = { "name": application_name }
            application_versions[application_id] = {}
        
        application_versions[application_id][application_version] = {}

        flash("%s version %s created." % (application_name, application_version))

        return redirect(url_for("list_applications"))

class ApplicationsView(MethodView):
    def list_applications(self):
        messages = get_flashed_messages()

        return render_template("index.html", applications=applications, application_versions=application_versions, messages=messages)
    
    def get(self):
        return self.list_applications()

@app.route("/releases/v1/new_application", methods=["GET", "POST"])
def create_application():
    if request.method == "GET":
        return render_template("new_application.html")


@app.route("/releases/v1/<application_id>/new_version", methods=["GET", "POST"])
def create_version(application_id):
    if not application_id in applications:
        return redirect(url_for("create_application"))

    requested_version = request.cookies.get("requested_version") or ""

    if request.method == "GET":
        response = make_response(render_template("new_version.html", applications=applications, selected_application_id=application_id, requested_version=requested_version))
        response.set_cookie("requested_version", "", expires=datetime.datetime(1970, 1, 1))

        return response

    errors = []

    application_version = request.form["application_version"] or ""
    if application_version.strip() == "":
        errors.append("Please enter a version number in <major.minor.patch> format.")

    if errors:
        return render_template("new_version", **locals())

    application_versions[application_id][application_version] = {}

    return redirect(url_for("edit_application", application_id=application_id, version=application_version))

@app.route("/releases/v1")
def list_applications():
    messages = get_flashed_messages()

    return render_template("index.html", applications=applications, application_versions=application_versions, messages=messages)

def edit_general_info(application_id, version):
    if request.method == "GET":
        return render_template("general_info.html", application_id=application_id, application_version=application_versions[application_id][version])

    application = applications[application_id]

    errors = []

    release_type = request.form["release_type"]
    if not release_type:
        errors.append("Please specify a release type.")

    num_enhancements = int(request.form["num_enhancements"].strip()) or 0
    num_bugfixes = int(request.form["num_bugfixes"].strip()) or 0

    if errors:
        #return render_template("general_info.html", application=application, version=version, errors=errors)
        return render_template("general_info.html", **locals())

    selected_version = application_versions[application_id][version]
    selected_version["release_type"] = release_type
    selected_version["num_enhancements"] = num_enhancements
    selected_version["num_bugfixes"] = num_bugfixes

    return redirect(url_for("edit_application", application_id=application_id, version=version))

@app.route("/releases/v1/<application_id>/<version>", methods=["GET", "POST"])
def edit_application(application_id, version):
    if not application_exists(application_id):
        return redirect(url_for("create_application"))

    if not version in application_versions[application_id]:
        response = make_response(redirect(url_for("create_version", application_id=application_id)))
        response.set_cookie("requested_version", version)

        return response

    section = request.args.get("section") or ""

    if section.strip() == "":
        return redirect(url_for("list_applications"))

    if section == "general_info":
        return edit_general_info(application_id, version)

    return render_template("application.html", application=applications[application_id], version=version)
