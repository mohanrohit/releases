# BaseController

from flask import request

from flask.ext.classy import FlaskView, route

class BaseController(FlaskView):
  __abstract__ = True

  route_base = "/"

  def __init__(self):
    self.params = {}

  def before_request(self, name, **kwargs):
    for key in request.values:
        self.params[key] = request.values[key]
