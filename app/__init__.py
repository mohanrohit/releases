from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from router import Router

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")

db = SQLAlchemy(app)

router = Router(app, db, type="mvc", trailing_slash=False, route_prefix="/releases/v1")
