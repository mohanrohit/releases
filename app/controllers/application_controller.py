# ApplicationController

from flask import render_template
from flask import url_for
from flask import redirect

from base_controller import *

from app.forms import NewApplicationForm

class ApplicationController(BaseController):
    def __init__(self):
        BaseController.__init__(self)

    @route("/applications")
    def index(self):
        applications = Application.query.all()

        return render_template("applications/index.html", applications=applications)

    @route("/applications/<int:id>")
    def get(self, id):
        application = Application.query.filter(Application.id == id).first()

        return render_template("applications/get.html", id=id, application=application)

    @route("/applications/new", methods=["GET", "POST"])
    def new(self):
        new_application_form = NewApplicationForm()

        if request.method == "GET":
            return render_template("applications/new.html", application_form=new_application_form)

        if new_application_form.validate_on_submit():
            application = Application(name=self.params["name"])
            application.save()
        else:
            print "validation failed"
            print new_application_form.errors

        return redirect(url_for("ApplicationController:index"))
