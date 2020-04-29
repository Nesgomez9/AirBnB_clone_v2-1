#!/usr/bin/python3
"""
New view for City objects that handles all default RestFul API actions
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_city(state_id):
    """Retrieves the list of all City objects of a State: GET"""
    state_req = storage.get('State', state_id)
    """If the state_id is not linked to any State object,"""
    if state_req is None:
        abort(404)
    cities = state_req.cities
    city_req = []
    for city in cities:
        city_req.append(city.to_dict())
    return jsonify(city_req)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_id(city_id):
    """method that retrieves a city filter by id"""
    city_req = storage.get('City', city_id)
    if city_req is None:
        abort(404)
    return jsonify(city_req.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_id(city_id):
    """Finde the id and then delete"""
    errase_city = storage.get('City', city_id)
    """If the city_id is not linked to any City object, raise a 404 error"""
    if not errase_city:
        abort(404)
    else:
        errase_city.delete()
        storage.save()
        """Returns an empty dictionary with the status code 200"""
        return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def post_city_by_state(state_id):
    """Creates a City: POST """
    my_state = storage.get('State', state_id)
    if my_state is None:
        abort(404)
    """to transform the HTTP body request to a dictionary"""
    new_city = request.get_json()
    if new_city is None:
        abort(400, 'Not a JSON')
    if 'name' not in new_city:
        abort(400, 'Missing name')
    new_city = City(name=request.json['name'], state_id=state_id)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def set_city(city_id):
    """Updates a City object: PUT"""
    req_city = request.get_json()
    if not request.json:
        abort(400, 'Not a JSON')
    mod_city = storage.get('City', city_id)
    if mod_city is None:
        abort(404)
    for key in req_city:
        if key == 'id' or key == 'created_at' or key == 'updated_at':
            pass
        else:
            setattr(mod_city, key, req_city[key])
    storage.save()
    return jsonify(mod_city.to_dict()), 200
