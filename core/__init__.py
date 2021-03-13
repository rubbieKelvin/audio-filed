from flask import Flask

from .extensions import mongo
from .main.routes import main

def create_app():
	app = Flask(__name__)

	app.config["SECRET_KEY"] = "IgF//\\O6\\o75\\xdO\x\\d7DFo68Frtly;9FDDOdlf;7fD6DOF8F7f"
	app.config["MONGO_URI"] = "mongodb+srv://me:i88uXJaR6RKTWhoX@audio-filed-cluster.ixpvo.mongodb.net/audio_filed_db?retryWrites=true&w=majority"

	mongo.init_app(app)

	app.register_blueprint(main)
	return app