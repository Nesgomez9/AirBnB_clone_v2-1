#!/usr/bin/python3
""" Amenity handles all default RestFul API actions """

from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity

@app_views.route("/amenities/<amenity_id>",
                 methods=["GET"],
                 strict_slashes=False)
@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amenity(amenity_id=None):
    if not amenity_id:
        """Retrieves the list of all Amenity objects: GET"""
        amenity_req = storage.all('Amenity')
        amenities_all = amenity_req.values()
        amenities_json = []
        for amenity in amenities_all:
            """to_dict() to serialize an object into valid JSON"""
            amenities_json.append(amenity.to_dict())
        return jsonify(amenities_json)
    else:
        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            abort(404)
        return jsonify(amenity.to_dict())

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                strict_slashes=False)
def delete_id(amenity_id):
    """Deletes a Amenity object:: DELETE """
    errase_amenity = storage.get('Amenity', amenity_id)
    if not errase_amenity:
        abort(404)
    errase_amenity.delete()
    storage.save()
    """Returns an empty dictionary with the status code 200"""
    return jsonify({}), 200
