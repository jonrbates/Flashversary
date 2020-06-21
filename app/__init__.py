# -*- coding: utf-8 -*-

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

application = Flask(__name__)   # application object
application.config.from_object(Config)
db = SQLAlchemy(application)
Migrate(application, db)
login = LoginManager(application)
login.login_view = 'login'

from app import routes, models, errors
