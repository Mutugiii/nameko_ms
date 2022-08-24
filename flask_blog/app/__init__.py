from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from config import config_options  

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()

def create_app(config_name):
  '''Application-factory format'''
  app = Flask(__name__)

  # Creating configurations
  app.config.from_object(config_options[config_name])

  # Initialize extensions
  db.init_app(app)
  bcrypt.init_app(app)
  migrate.init_app(app, db)

  # Registering blueprints
  from .main import main as main_blueprint
  app.register_blueprint(main_blueprint, url_prefix='/v1/main')

  from .auth import auth as auth_blueprint
  app.register_blueprint(auth_blueprint, url_prefix='/v1/auth')

  # Allow flask db to detect the models for migrations
  from app.models import UserModel, BlogModel

  return app
  