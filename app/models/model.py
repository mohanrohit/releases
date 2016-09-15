# model.py -- the (abstract) Model from which all models derive

from app import db

class Model(db.Model):
  __abstract__ = True

  def save(self):
    db.session.add(self)
    db.session.commit()
