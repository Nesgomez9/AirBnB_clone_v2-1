#!/usr/bin/python3
"""Index of the API"""
from flask import jsonify
from api.v1.views import app_views


Classes = [Amenity, City, Place, Review, State, User]


@app_views.route("/status", strict_slashes=False)
def status():
    """Status"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def stats():
    """Return the number of objects of a class"""
    strings = ["amenities", "cities", "places", "reviews", "states", "users"]
    dic_count = {}
    for i in range(len(classes)):
        dic_count[strings[i]] = storage.count(classes[i])
    return jsonify(dic_count)
