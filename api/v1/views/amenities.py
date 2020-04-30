#!/usr/bin/python3
""" Amenity handles all default RestFul API actions """

from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """method that retrieves a list of all amenities"""
    all_amenities = storage.all('Amenity')
    amenities_list = all_amenities.values()
    amenities_json = []
    for amenity in amenities_list:
        amenities_json.append(amenity.to_dict())
    return jsonify(amenities_json)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity_by_id(amenity_id):
    """method that retrieves a state filter by id"""
    my_amenity = storage.get('Amenity', amenity_id)
    if my_amenity is None:
        abort(404)
    return jsonify(my_amenity.to_dict())

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_id(amenity_id):
    """Deletes a Amenity object:: DELETE """
    errase_amenity = storage.get('Amenity', amenity_id)
    if not errase_amenity:
        abort(404)
    else:
        errase_amenity.delete()
        storage.save()
        """Returns an empty dictionary with the status code 200"""
        return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """Creates a Amenity: POST"""
    post_amenity = request.get_json()
    if post_amenity is None:
        abort(400, 'Not a JSON')
    if 'name' not in post_amenity:
        abort(400, 'Missing name')
    """ to transform the HTTP request to a dictionary"""
    post_amenity = Amenity(name=request.json['name'])
    storage.new(post_amenity)
    storage.save()
    return jsonify(post_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """Updates a Amenity object: PUT"""
    put_amenity = request.get_json()
    if not request.json:
        abort(400, 'Not a JSON')
    mod_amenity = storage.get('Amenity', amenity_id)
    if mod_amenity is None:
        abort(404)
    for key in put_amenity:
        if key == 'id' or key == 'created_at' or key == 'updated_at':
            pass
        else:
            setattr(mod_amenity, key, put_amenity[key])
    storage.save()
    return jsonify(mod_amenity.to_dict()), 200
