# ...
import os
from flask import Flask

# ...
from .extensions import mongo
from .main.routes import main

# ... for environmental varibles
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

# ...
def create_app() -> Flask:

	""" create a flask application instance.
	"""

	app = Flask(__name__)

	# set application configuration
	app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
	app.config["MONGO_URI"] = os.getenv("MONGO_URI")

	# initialize flask extensions
	mongo.init_app(app)

	# register blueprints
	app.register_blueprint(main)

	return app
