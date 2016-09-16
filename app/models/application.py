# application.py -- the Application model representing the applications in the system

from model import Model, db

class Application(Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    name = db.Column(db.String, nullable=False, unique=True)

    def __init__(self, **kwargs):
        Model.__init__(self, **kwargs)

    def __repr__(self):
        return self.name
