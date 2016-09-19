# application.py -- the Application model representing the applications in the system

from model import Model, db

class Application(Model):
    __tablename__ = "applications"

    id = db.Column(db.String, primary_key=True, index=True, unique=True)
    name = db.Column(db.String, nullable=False, unique=True)
    versions = db.relationship("Version", backref="application", lazy="dynamic")

    def __init__(self, **kwargs):
        Model.__init__(self, **kwargs)

    def __repr__(self):
        return self.name
