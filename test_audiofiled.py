import pytest
from random import randint
from flask.testing import FlaskClient
from core import create_app

app = create_app()
NEWLY_CREATED = []

@pytest.fixture
def client():
	app.config["TESTING"] = True
	
	with app.test_client() as client:
		yield client


def test_get(client: FlaskClient):
	resps_ = [client.get(f'/resource/{type_}') for type_ in ["song", "podcast", "audiobook"]]

	for resp in resps_:
		assert type(resp.json) == list

def test_post(client: FlaskClient):
	song = dict(
		audioFileType="song",
		audioFileMetadata=dict(
			name="test_",
			duration=20,
		)
	)

	podcast = dict(
		audioFileType="podcast",
		audioFileMetadata=dict(
			name="test name",
			duration=20,
			host="test_host",
			participants=[ f"participant {x}" for x in range(9) ]
		)
	)

	audioBook = dict(
		audioFileType="audiobook",
		audioFileMetadata=dict(
			name="test name",
			duration=20,
			author="test author",
			narrator="test naratorr"
		)
	)

	for json in [song, podcast, audioBook]:
		res = client.post("/resource", json=json)
		data : dict = res.json

		assert data.get("_id") != None

		# we'll delete these later
		NEWLY_CREATED.append((json.get("audioFileType"), data.get("_id").get("$oid")))

def test_delete(client: FlaskClient):
	from bson import ObjectId

	for type_, id_ in NEWLY_CREATED:
		resp = client.delete(f"/resource/{type_}/{id_}")
		assert resp.status == "204 NO CONTENT"
