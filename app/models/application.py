# application.py -- the Application model representing the applications in the system

import datetime

from model import Model, db

class Application(Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False, autoincrement=True, index=True)
    slug = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    versions = db.relationship("Version", backref="application", lazy="dynamic")

    @staticmethod
    def get_by_slug(slug):
        return Application.query.filter(Application.slug == slug).first()

    def __init__(self, **kwargs):
        Model.__init__(self, **kwargs)

    def __repr__(self):
        return self.name
