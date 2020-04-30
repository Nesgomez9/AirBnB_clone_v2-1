#!/usr/bin/python3
"""Place objects that handles all default RestFul API actions:"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_all(city_id):
    """Retrieves the list of all Review objects of a Place: GET"""
    my_city = storage.get('City', city_id)
    if my_city is None:
        abort(404)
    places = my_city.places
    places_list = []
    for place in places:
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_id(place_id):
    """Retrieves the list of all Review objects of a Place: GET by id"""
    my_place = storage.get('Place', place_id)
    if my_place is not None:
        return jsonify(my_place.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_id(place_id):
    """Deletes a Review object: DELETE"""
    delete_place = storage.get('Place', place_id)
    if delete_place is None:
        abort(404)
    storage.delete(delete_place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_review(city_id):
    """Creates a Review: POST"""
    new_place = request.get_json()
    if not new_place:
        abort(400, 'Not a JSON')
    if 'user_id' not in new_place:
        abort(400, 'Missing user_id')
    if 'name' not in new_place:
        abort(400, 'Missing name')
    my_city = storage.get('City', city_id)
    if my_city is None:
        abort(404)

    my_user = storage.get('User', request.json['user_id'])
    if my_user is None:
        abort(404)

    new_place = Place(name=request.json['name'],
                      city_id=city_id, user_id=request.json['user_id'])
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_review(place_id):
    """Updates a Review object: PUT"""
    mod_place = storage.get('Place', place_id)
    if mod_place is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    req_place = request.get_json()
    for key in req_place:
        if key == 'id' or key == 'user_id' or\
           key == 'city_id' or key == 'created_at' or key == 'updated_at':
            pass
        else:
            setattr(mod_place, key, req_place[key])
    storage.save()
    return jsonify(mod_place.to_dict()), 200
