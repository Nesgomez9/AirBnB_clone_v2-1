#!/usr/bin/python3
"""Index of the API"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User



@app_views.route("/status", strict_slashes=False)
def status():
    """Status"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def stats():
    """Return the number of objects of a class"""
    strings = ["amenities", "cities", "places", "reviews", "states", "users"]
    classes = [Amenity, City, Place, Review, State, User]
    dic_count = {}
    for i in range(len(classes)):
        dic_count[strings[i]] = storage.count(classes[i])
    return jsonify(dic_count)
