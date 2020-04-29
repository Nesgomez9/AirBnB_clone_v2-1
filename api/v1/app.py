#!/usr/bin/python3
"""Module to create a API with flask"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_storage(self):
    """closes the storage"""
    storage.close()

if __name__ == "__main__":
    app.run(host= getenv("HBNB_API_HOST"),
            port=getenv("HBNB_API_PORT"),
            threaded=True)
