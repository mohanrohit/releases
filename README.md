# releases

2016-09-16
----------

added versions to application. need to associate one application with multiple versions, so versions must be a separate table.
it contains major, minor, patch and build version numbers along with the application id as the foreign key

# version.py -- the Version model representing a version of an application

import re

from model import Model, db

class Version(Model):
    __tablename__ = "versions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)

    major = db.Column(db.Integer, nullable=False, default=1)
    minor = db.Column(db.Integer, nullable=False, default=0)
    patch = db.Column(db.Integer, nullable=False, default=0)
    build = db.Column(db.Integer, nullable=False, default=0)

    application_id = db.Column(db.Integer, db.ForeignKey("applications.id"))

    def __init__(self, **kwargs):
        Model.__init__(self, **kwargs)

    def __repr__(self):
        return "%d.%d.%d.%d" % (self.major, self.minor, self.patch, self.build)

    @staticmethod
    def parse(version_string):
        """parses version string that must be in the form major.minor.patch.build"""

        match = re.search(r"(\d+)\.(\d+)(?:\.(\d+))?(?:\.(\d+))?", version_string)
        if match:
            captures = match.groups()

            return {
                "major": int(captures[0]),
                "minor": int(captures[1]),
                "patch": int(captures[2]) if captures[2] else 0,
                "build": int(captures[3]) if captures[3] else 0
            }

        return {}

then run python manage.py db upgrade and it adds a migration to the list of migrations and
creates the new versions table.

2016-09-19
----------
    def get(self, id):
        application = Application.query.filter(Application.id == id).first()
        versions = Version.query(Application.id == Version.application_id)

        return render_template("applications/get.html", id=id, application=application, versions=versions)

getting the same versions for all applications. realized it should be:

    def get(self, id):
        application = Application.query.filter(Application.id == id).first()
        versions = Version.query(application.id == Version.application_id) # smallcase 'a' for the application object just retrieved

        return render_template("applications/get.html", id=id, application=application, versions=versions)

used flask-logging to figure out what was going on.

corrected it to:

    def get(self, id):
        application = Application.query.filter(Application.id == id).first()
        versions = Version.query(application.id == Version.application_id)

        return render_template("applications/get.html", id=id, application=application, versions=versions)

but then i realized the right way to do it would be to use the versions attribute of the application object

    def get(self, id):
        application = Application.query.filter(Application.id == id).first()
        versions = application.versions

        return render_template("applications/get.html", id=id, application=application, versions=versions)


