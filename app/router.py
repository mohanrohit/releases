# router.py -- adds routing to Flask app

import os
import sys

import re
import importlib
import inflect

class Router(object):
  class ApplicationType(object):
    MVC = 0 # conventional -- Model-View-Controller
    MTV = 1 # default for Flask apps -- Model-Template-View

  def get_application_type(self, args):
    type = args.pop("type", "mtv")

    if not type.upper() in ("MTV", "MVC"):
      return Router.ApplicationType.MTV

    if type.upper() == "MTV":
      return Router.ApplicationType.MTV

    if type.upper() == "MVC":
      return Router.ApplicationType.MVC

    return Router.ApplicationType.MTV

  def get_controllers_path(self, args):
    if "views_path" in args:
      return args["views_path"]

    if "controllers_path" in args:
      return args["controllers_path"]

    if self.application_type == Router.ApplicationType.MTV:
      return os.path.dirname(__file__) + "/views"

    if self.application_type == Router.ApplicationType.MVC:
      return os.path.dirname(__file__) + "/controllers"

    return os.path.dirname(__file__) + "/views"

  def get_controller_class_name(self, controller_module_name):
    separator_pos = controller_module_name.index("_")

    return controller_module_name[0:separator_pos].capitalize() + controller_module_name[separator_pos:].capitalize()

  def get_controller_module_name(self, controller_file_name):
    return os.path.splitext(controller_file_name)[0]

  def get_controller_modules(self, controllers_path):
    sys.path.append(controllers_path)

    all_files = os.listdir(controllers_path)

    if self.application_type == Router.ApplicationType.MTV:
      controllers_regex = re.compile(r"(.*)_(view)\.py$", re.IGNORECASE)
    else:
      controllers_regex = re.compile(r"(.*)_(controller)\.py$", re.IGNORECASE)

    controller_files_names = filter(controller_regex.search, all_files)

    for controller_file_name in controller_file_names:
      controller_module_name = self.get_controller_module_name(controller_files_name)
      controller_class_name = self.get_controller_class_name(controller_module_name)

      controller_module = self.import_module(controller_module_name)

    controller_module_names = map(self.controller_module_name_from_file_name, controller_files_names)
    for controller_module_name in controller_module_names:
        yield controller_module_name

  def get_model_module_name(self, model_file_name):
    return os.path.splitext(model_file_name)[0]

  def get_model_class_name(self, model_module_name):
    return model_module_name.lower().capitalize()

  def get_models_path(self, args):
    if "models_path" in args:
      return args["models_path"]

    return os.path.dirname(__file__) + "/models"

  def import_models(self, models_path):
    models = []

    sys.path.insert(0, models_path)

    all_files = os.listdir(models_path)

    models_regex = re.compile(r"\.py$", re.IGNORECASE)

    model_file_names = filter(models_regex.search, all_files)

    model_module_names = map(self.get_model_module_name, model_file_names)
    model_class_names = map(self.get_model_class_name, model_module_names)

    for model_module_name, model_class_name in zip(model_module_names, model_class_names):
      model_module = importlib.import_module(model_module_name)

      # inject the database into each model's module, so it doesn't
      # have to be explicitly imported
      setattr(model_module, "db", self.db)

      model_class = model_module.__getattribute__(model_class_name)

      models.append(model_class)

    return models

  def get_controller_module_name(self, controller_file_name):
    return os.path.splitext(controller_file_name)[0]

  def get_controller_class_name(self, controller_module_name):
    separator_pos = controller_module_name.index("_")

    return controller_module_name[0:separator_pos].capitalize() + controller_module_name[separator_pos + 1:].capitalize()

  def import_controllers(self, controllers_path):
    controllers = []

    sys.path.insert(0, controllers_path)

    all_files = os.listdir(controllers_path)

    if self.application_type == Router.ApplicationType.MTV:
      controllers_regex = re.compile(r"(.*)_(view)\.py$", re.IGNORECASE)
    else:
      controllers_regex = re.compile(r"(.*)_(controller)\.py$", re.IGNORECASE)

    controller_file_names = filter(controllers_regex.search, all_files)

    controller_module_names = map(self.get_controller_module_name, controller_file_names)
    controller_class_names = map(self.get_controller_class_name, controller_module_names)

    for controller_module_name, controller_class_name in zip(controller_module_names, controller_class_names):
      controller_module = importlib.import_module(controller_module_name)
      controller_class = controller_module.__getattribute__(controller_class_name)

      controllers.append({"class": controller_class, "module": controller_module})

    return controllers

  def get_route_base(self, controller_class_name):
    # first strip out the -View or -Controller prefix (those are the
    # only we'll get -- we explicitly searched for only those two. see
    # import_controllers
    base_name = re.sub("(?:View|Controller)", "", controller_class_name)
    base_name = base_name.lower()

    singular_base_name = self.inflect.singular_noun(base_name)
    if singular_base_name == False: # already singular
      route_base = self.inflect.plural_noun(base_name)
    else:
      route_base = self.inflect.plural_noun(singular_base_name)

    return route_base

  def is_class_abstract(self, cls):
    abstract_attribute = "__abstract__"

    for base_class in cls.__bases__:
      base_class_is_abstract = getattr(base_class, "__abstract__", False)
      if base_class_is_abstract:
        return False

    # no base class had the __abstract__ attribute, check on the given class
    class_is_abstract = getattr(cls, "__abstract__", False)
    if class_is_abstract:
      return True

    return False

  def __init__(self, app, db, **kwargs):
    # use an inflection engine for generating route bases --
    # making plurals of controller names etc.
    self.inflect = inflect.engine()
    self.inflect.classical()

    self.app = app
    self.db = db

    self.application_type = self.get_application_type(kwargs)

    models = self.import_models(self.get_models_path(kwargs))

    controllers = self.import_controllers(self.get_controllers_path(kwargs))
    for controller in controllers:
      # inject each model into the controller's module so it can be
      # referenced without having to do an import...
      controller_module = controller["module"]
      for model in models:
        setattr(controller_module, model.__name__, model)

      # ... then register the controller to provide routes for the app
      controller_class = controller["class"]
      if not self.is_class_abstract(controller_class):
        route_base = controller_class.route_base if controller_class.route_base else self.get_route_base(controller_class.__name__)

        controller_class.register(app, route_base=route_base, **kwargs)
      
    for rule in self.app.url_map.iter_rules():
      print rule, rule.defaults, rule.arguments, rule.endpoint

if __name__ == "__main__":
    r = Router(None, type="mtv")
