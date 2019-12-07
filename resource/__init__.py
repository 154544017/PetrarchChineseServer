from flask import Flask
from . import hello

def create_app():
	app = Flask(__name__)

	@app.route('/')
	def init():
		return "init page"

	app.register_blueprint(hello.hellobp)
	return app
