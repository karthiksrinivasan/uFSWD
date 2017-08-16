from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import logging.config
from flask_restless import APIManager
import os
# Initializing the Flask App
server = Flask(__name__, static_url_path='/static', static_folder="static")
# Loading the Configuration

server.config.from_object(os.environ.get("ITEM_CATALOG_SERVER",
				     "app.config.DevelopmentConfig"))
# Connector object to the database
db_connector = SQLAlchemy(server)

login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = "users.login"
server_logger = logging.getLogger()

# Flask-Restless Object
restless_manager = APIManager(server, flask_sqlalchemy_db=db_connector)

from app import modules
