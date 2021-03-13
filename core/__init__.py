from flask import Flask

from .extensions import mongo
from .main.routes import main

def create_app():
	app = Flask(__name__)

	app.config["SECRET_KEY"] = "%E*&DI%6s6di5di5idi5u6su65dI75diTDdtTYDKdi56"
	app.config["MONGO_URI"] = "mongodb+srv://me:i88uXJaR6RKTWhoX@audio-filed-cluster.ixpvo.mongodb.net/audio_filed_db?retryWrites=true&w=majority"

	mongo.init_app(app)

	app.register_blueprint(main)
	return app