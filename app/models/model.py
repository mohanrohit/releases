# model.py -- the (abstract) Model from which all models derive

from app import db

class Model(db.Model):
    __abstract__ = True

    @classmethod
    def exists(cls, id):
        model = cls.query.get(id)

        return True if model else False

    def save(self):
        db.session.add(self)
        db.session.commit()
