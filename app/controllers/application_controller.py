# ApplicationController

from flask import render_template

from base_controller import *

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

    @route("/applications", methods=["POST"])
    def post(self):
        if not "name" in self.params:
            return jsonify(error="Title is required."), 400

        application = Application(title=self.params["title"])
        print "created new application: %s" % application
        application.save()

        return jsonify(**self.params)
