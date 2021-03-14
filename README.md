# Audio filed
Flask API that `"simulates"` the behavior of an audio file server, using a MongoDB database.


## Setup
- Python version: python 3.8

```bash
virtualenv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

## Run
```bash
flask run
```

## Tests
```bash
pytest -s
```

## Hosted url
```
https://audio-filed.herokuapp.com/

```

## Postman API Doc
```
https://documenter.getpostman.com/view/13988113/Tz5qadAs
```

## Stack
This project takes advantage of Flask and PyMongo as a Mongo DB driver. All libraries are in stable versions and are included in requirements.txt