from . import rules

from flask import request
from flask import Blueprint

from flask_restful import Api
from flask_restful import Resource

from core.extensions import mongo

from pymongo import errors
from datetime import datetime

from json import loads

from bson import ObjectId
from bson.json_util import dumps
from bson.errors import InvalidId

main = Blueprint('main', __name__)
api = Api(main)



class NewAudioResource(Resource):
	"""
	"""
	def post(self):
		data: dict = request.json

		audioFileType: str = data.get("audioFileType")

		if audioFileType == None or type(audioFileType) != str:
			return dict(), 400

		elif audioFileType.lower() == "song":
			# perform post actions for "song" types
			collection = mongo.db.song_collection
			ruler = rules.newSongRule

		elif audioFileType.lower() == "podcast":
			# perform post actions for "podcast" types
			collection = mongo.db.podcast_collection
			ruler = rules.newPodcastRule

		elif audioFileType.lower() == "audiobook":
			# perform post actions for "audiobook" types
			collection = mongo.db.audiobook_collection
			ruler = rules.newAudioBookRule

		else:
			# no specified type
			return dict(error="audio type not speified"), 400

		if ruler.compare(data):
			meta = data.get("audioFileMetadata")
			meta["uploadTime"] = datetime.utcnow()

			created_id = collection.insert_one(meta).inserted_id
			created = collection.find_one({"_id":created_id})
			
			return loads(dumps(created))

		return dict(error="data fields are invalid"), 400



class HandleAudioResource(Resource):
	"""
	"""
	def get(self, audioFile_type: str, audioFile_id: str = None) -> dict:
		audioFile_type = audioFile_type.lower()

		if audioFile_type == "song":
			collection = mongo.db.song_collection
		elif audioFile_type == "podcast":
			collection = mongo.db.podcast_collection
		elif audioFile_type == "audiobook":
			collection = mongo.db.audiobook_collection
		else:
			# no specified type
			return dict(error="audio type not speified"), 400

		if audioFile_id == None:
			# get all the audio files of $audioFile_type
			items = collection.find()
			return loads(dumps(items))

		try:
			item = collection.find_one({"_id": ObjectId(audioFile_id)})
		except InvalidId:
			return dict(error="invalid id"), 400

		if item==None:
			return dict(error="resource not found"), 404
		return loads(dumps(item))



	def patch(self, audioFile_type: str, audioFile_id: int = None) -> dict:
		if (audioFile_id == None):
			return dict(msg="provide audioFile_id"), 400

		data: dict = request.json

		audioFileType: str = data.get("audioFileType")

		if audioFileType == None or type(audioFileType) != str:
			return dict(), 400

		elif audioFileType.lower() == "song":
			# perform post actions for "song" types
			collection = mongo.db.song_collection
			ruler = rules.newSongRule

		elif audioFileType.lower() == "podcast":
			# perform post actions for "podcast" types
			collection = mongo.db.podcast_collection
			ruler = rules.newPodcastRule

		elif audioFileType.lower() == "audiobook":
			# perform post actions for "audiobook" types
			collection = mongo.db.audiobook_collection
			ruler = rules.newAudioBookRule

		else:
			# no specified type
			return dict(error="audio type not speified"), 400

		if ruler.compare(data):
			meta = data.get("audioFileMetadata")
			
			try:
				item: dict = collection.find_one({"_id": ObjectId(audioFile_id)})
			except InvalidId:
				return dict(error="invalid id"), 400

			item.update(meta)
			collection.save(meta)

			return loads(dumps(item))

		return dict(error="data fields are invalid"), 400



	def delete(self, audioFile_type: str, audioFile_id: int = None) -> dict:
		if (audioFile_id == None):
			return dict(msg="provide audioFile_id"), 400

		audioFile_type = audioFile_type.lower()

		if audioFile_type == "song":
			collection = mongo.db.song_collection
		elif audioFile_type == "podcast":
			collection = mongo.db.podcast_collection
		elif audioFile_type == "audiobook":
			collection = mongo.db.audiobook_collection
		else:
			# no specified type
			return dict(error="audio type not speified"), 400

		try:
			collection.delete_many({"_id": ObjectId(audioFile_id)})
		except InvalidId:
			return dict(error="invalid id"), 400

		return dict(msg="deleted audio resource"), 204


api.add_resource(NewAudioResource, "/resource")
api.add_resource(HandleAudioResource, "/resource/<string:audioFile_type>/<string:audioFile_id>", "/resource/<string:audioFile_type>")
