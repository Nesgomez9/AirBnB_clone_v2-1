#!/usr/bin/python3
"""User object that handles all default RestFul API actions"""

from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all():
    """Retrieves the list of all User objects: GET"""
    all_users = storage.all('User')
    users_list = all_users.values()
    users_json = []
    for user in users_list:
        users_json.append(user.to_dict())
    return jsonify(users_json)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    """Retrieves the list of all User objects: GET"""
    my_user = storage.get('User', user_id)
    if my_user is None:
        abort(404)
    return jsonify(my_user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    """Deletes a User object:: DELETE """
    delete_user = storage.get('User', user_id)
    if not delete_user:
        abort(404)
    else:
        delete_user.delete()
        storage.save()
        return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """Creates a User: POST"""
    new_user = request.get_json()
    if new_user is None:
        abort(400, 'Not a JSON')
    if 'email' not in new_user:
        abort(400, 'Missing email')
    if 'password' not in new_user:
        abort(400, 'Missing password')
    new_user = User(email=request.json['email'],
                    password=request.json['password'])
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def put_user(user_id):
    """Updates a User object: PUT """
    req_user = request.get_json()
    if not request.json:
        abort(400, 'Not a JSON')
    mod_user = storage.get('User', user_id)
    if mod_user is None:
        abort(404)
    for key in req_user:
        if key == 'id' or key == 'email' or\
           key == 'created_at' or key == 'updated_at':
            pass
        else:
            setattr(mod_user, key, req_user[key])
    storage.save()
    return jsonify(mod_user.to_dict()), 200
