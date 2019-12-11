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
<<<<<<< HEAD
		from .controller import userApi,helloApi,textLibApi,dictionaryApi
		app.register_blueprint(helloApi.hellobp)
		app.register_blueprint(blueprint=userApi.user_api, url_prefix='/user')
		app.register_blueprint(blueprint=textLibApi.textLib_api, url_prefix='/textlibrary')
		app.register_blueprint(blueprint=dictionaryApi.dictionary_api, url_prefix='/dic')
=======
		from .controller import userApi,helloApi,dictionaryApi
		app.register_blueprint(helloApi.hellobp)
		app.register_blueprint(blueprint=userApi.user_api, url_prefix='/user')
		app.register_blueprint(blueprint=dictionaryApi.dictionary_api, url_prefix='/dic')
>>>>>>> 282b82a5fd7cadea4f0d6e37e060cb1c2920d90b
		# Create tables for our models
		db.create_all()
		return app
