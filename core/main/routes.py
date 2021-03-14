# rules
from . import rules

# flask
from flask import request, Blueprint

# flask restful
from flask_restful import Api, Resource

# extensions
from core.extensions import mongo

# pymongo
from pymongo import errors

# builtins
from json import loads
from datetime import datetime

# bson for mongodb
from bson import ObjectId
from bson.json_util import dumps
from bson.errors import InvalidId


SONG = "song"
PODCAST = "podcast"
AUDIOBOOK = "audiobook"



# create blue print instance
main = Blueprint('main', __name__)

# register rest-api under this blueprint
api = Api(main)



class NewAudioResource(Resource):
	""" Contains end point for creating new audio resource 
	"""

	def post(self):
		# create new audio recource,

		# get json body
		data: dict = request.json

		if data is None:
			# there's no body
			# just return a bad request response
			return dict(error="no value in request body"), 400

		# get audio type
		# the default is song
		audioFileType: str = data.get("audioFileType", SONG).lower()


		if audioFileType == SONG:
			# create a SONG audio resource
			# set collection & rule (model) to satisfy SONG type
			collection = mongo.db.song_collection
			ruler = rules.newSongRule

		elif audioFileType == PODCAST:
			# create a PODCAST audio resource
			# set collection & rule (model) to satisfy PODCAST type
			collection = mongo.db.podcast_collection
			ruler = rules.newPodcastRule

		elif audioFileType == AUDIOBOOK:
			# create a AUDIOBOOK audio resource
			# set collection & rule (model) to satisfy AUDIOBOOK type
			collection = mongo.db.audiobook_collection
			ruler = rules.newAudioBookRule

		else:
			# unknown type
			# return error
			return dict(error=f"type {audioFileType} not known. known types are 'song', 'podcast', 'audiobook'."), 400

		# if all things are good,
		# compare data with specified rule.  
		if ruler.compare(data):

			# meta contains properties for the new audio resource
			meta = data.get("audioFileMetadata")

			# set upload time to now
			meta["uploadTime"] = datetime.utcnow()

			# fetch created id; used to retrieve object data back from mongo
			created_id = collection.insert_one(meta).inserted_id
			created = collection.find_one({"_id":created_id})
			
			# return a json serializable version of bson string.
			return loads(dumps(created))

		return dict(error="data fields are invalid"), 400



class HandleAudioResource(Resource):
	""" Contains classes for the 3 other endpoints.
	
	$get: retreives descr data from the database. if id is not specified.
	--returns all audio data under specified type.
	
	$patch: edits audio information.
	
	$delete: removes specified audio.
	"""
	
	def get(self, audioFile_type: str, audioFile_id: str = None) -> dict:
		"""retreives descr data from the database."""

		# audio file type, all case lowered to avoid conflict.
		audioFile_type = audioFile_type.lower()

		# mapp audio file type to collection
		if audioFile_type == SONG:
			collection = mongo.db.song_collection

		elif audioFile_type == PODCAST:
			collection = mongo.db.podcast_collection
		
		elif audioFile_type == AUDIOBOOK:
			collection = mongo.db.audiobook_collection
		
		else:
			# unknown type
			# return error
			return dict(error=f"type {audioFile_type} not known. known types are 'song', 'podcast', 'audiobook'."), 400

		if audioFile_id == None:
			# get all the audio files of $audioFile_type
			items = collection.find()
			return loads(dumps(items))

		# try getting item
		# expected errors:
		# --> InvalidId: id is not a valid bson.ObjectId 
		try:
			item = collection.find_one({"_id": ObjectId(audioFile_id)})

			if item:
				return loads(dumps(item))

		except InvalidId:
			pass

		return dict(error="resource not found"), 404



	def patch(self, audioFile_type: str, audioFile_id: int = None) -> dict:

		# all case lower to avoid conflict
		audioFile_type = audioFile_type.lower()

		# audiofile_id must be specified
		if (audioFile_id == None):
			return dict(error="provide audioFile_id"), 400

		data: dict = request.json

		if data is None:
			# there's no body
			# just return a bad request response
			return dict(error="no value in request body"), 400

		if audioFile_type == SONG:
			# perform post actions for SONG types
			collection = mongo.db.song_collection
			ruler = rules.patchSongRule

		elif audioFile_type == PODCAST:
			# perform post actions for PODCAST types
			collection = mongo.db.podcast_collection
			ruler = rules.patchPodcastRule

		elif audioFile_type == AUDIOBOOK:
			# perform post actions for AUDIOBOOK types
			collection = mongo.db.audiobook_collection
			ruler = rules.patchAudioBookRule

		else:
			# unknown type
			# return error
			return dict(error=f"type {audioFile_type} not known. known types are 'song', 'podcast', 'audiobook'."), 400

		# if body is valid
		if ruler.compare(data):
			
			try:
				item: dict = collection.find_one({"_id": ObjectId(audioFile_id)})
			except InvalidId:
				return dict(error="item not found"), 404

			# update and save data
			item.update(data)
			collection.save(item)

			return loads(dumps(item))

		return dict(error="data fields are invalid"), 400



	def delete(self, audioFile_type: str, audioFile_id: int = None) -> dict:
		# all case lower to avoid conflict
		audioFile_type = audioFile_type.lower()

		# audiofile_id must be specified
		if (audioFile_id == None):
			return dict(error="provide audioFile_id"), 400

		if audioFile_type == SONG:
			collection = mongo.db.song_collection

		elif audioFile_type == PODCAST:
			collection = mongo.db.podcast_collection

		elif audioFile_type == AUDIOBOOK:
			collection = mongo.db.audiobook_collection
		
		else:
			# unknown type
			# return error
			return dict(error=f"type {audioFile_type} not known. known types are 'song', 'podcast', 'audiobook'."), 400

		try:
			collection.delete_one({"_id": ObjectId(audioFile_id)})
		except InvalidId:
			pass
		
		return None, 204


api.add_resource(NewAudioResource, "/resource")
api.add_resource(HandleAudioResource, "/resource/<string:audioFile_type>/<string:audioFile_id>", "/resource/<string:audioFile_type>")
