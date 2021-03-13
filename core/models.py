from . import db
from datetime import datetime


class AudioResource (db.Document):
	name = db.StringField()