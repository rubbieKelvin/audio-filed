from maprule import fields

# RULES FOR "CREATE" ENDPOINT
newSongRule = fields.Dictionary(dict(
	audioFileType=fields.String(validate=lambda x:x.lower()=="song"),
	audioFileMetadata=fields.Dictionary(dict(
		name=fields.String(min_length=1, max_length=100),
		duration=fields.Integer(minimum=0),
	))
))

newPodcastRule = fields.Dictionary(dict(
	audioFileType=fields.String(validate=lambda x:x.lower()=="podcast"),
	audioFileMetadata=fields.Dictionary(dict(
		name=fields.String(min_length=1, max_length=100),
		duration=fields.Integer(minimum=0),
		host=fields.String(min_length=1, max_length=100),
		participants=fields.Array(fields.String(min_length=1, max_length=100), validate=lambda x: len(x) <= 10, nullable=True)
	))
))

newAudioBookRule = fields.Dictionary(dict(
	audioFileType=fields.String(validate=lambda x:x.lower()=="audiobook"),
	audioFileMetadata=fields.Dictionary(dict(
		name=fields.String(min_length=1, max_length=100),
		duration=fields.Integer(minimum=0),
		author=fields.String(min_length=0, max_length=100),
		narrator=fields.String(min_length=0, max_length=100)
	))
))

