from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from resource.controller import helloApi
from . import config

app = Flask(__name__)
db = SQLAlchemy()


def create_app():
	app.config.from_object(config.Config)
	db.init_app(app)
	with app.app_context():
		# Imports
		from .controller import userApi,helloApi
		app.register_blueprint(helloApi.hellobp)
		app.register_blueprint(blueprint=userApi.user_api, url_prefix='/user')
		# Create tables for our models
		db.create_all()
		return app
