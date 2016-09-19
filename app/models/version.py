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

    application_id = db.Column(db.String, db.ForeignKey("applications.id"))

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
