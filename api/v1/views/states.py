#!/usr/bin/python3
"""State request methods handler"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states(state_id=None):
    """GET request"""
    states_list = []
    if not state_id:
        states = storage.all(State).values()
        for state in states:
            states_list.append(state.to_dict())
        return jsonify(states_list)
    else:
        state = storage.get(State, state_id)
        if not state:
            abort(404)
        return jsonify(state.to_dict())


@app_views.route("/states/<state_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def delete_states(state_id):
    """DELETE request"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def post_states():
    """POST request"""
    info = request.get_json()
    if not info:
        abort(400, "Not a JSON")
    if "name" not in info:
        abort(400, "Missing name")
    new = State(**info)
    new.save()
    return jsonify(new.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def put_states(state_id):
    """PUT request"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    info = request.get_json()
    if not info:
        abort(400, "Not a JSON")
    for key, value in info.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
