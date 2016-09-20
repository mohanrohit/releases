# version.py -- the Version model representing a version of an application

import re
import datetime

from model import Model, db

class Version(Model):
    __tablename__ = "versions"

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, autoincrement=True, index=True)
    spec = db.Column(db.String, default="1.0", nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    application_id = db.Column(db.String, db.ForeignKey("applications.id"), nullable=False)

    def __init__(self, **kwargs):
        Model.__init__(self, **kwargs)

    def __repr__(self):
        return spec

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
