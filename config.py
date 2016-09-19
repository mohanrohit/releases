import os

base_directory = os.path.abspath(os.path.dirname(__file__))

class Config(object):
  DEBUG = False
  TESTING = False
  WTF_CSRF_ENABLED = True
  SECRET_KEY = "some-secret-key"

  # for SQLAlchemy
  SQLALCHEMY_DATABASE_URI = "sqlite:///" + base_directory + "/db/release_plan.db"
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SQLALCHEMY_MIGRATE_REPO = base_directory + "/db/migrations"
  SQLALCHEMY_ECHO = True # print SQL statements for debugging

class ProductionConfig(Config):
  DEBUG = False

class StagingConfig(Config):
  DEVELOPMENT = True
  DEBUG = True

class DevelopmentConfig(Config):
  DEVELOPMENT = True
  DEBUG = True

class TestingConfig(Config):
  TESTING = True
