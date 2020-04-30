#!/usr/bin/python3
"""
Reviews CRUD
"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews_by_place(place_id):
    """method that retrieves a list of all states"""
    my_place = storage.get('Place', place_id)
    if my_place is None:
        abort(404)
    reviews = my_place.reviews
    reviews_list = []
    for review in reviews:
        reviews_list.append(review.to_dict())
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review_by_id(review_id):
    """method that retrieves a review filter by id"""
    my_review = storage.get('Review', review_id)
    if my_review is not None:
        return jsonify(my_review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_reviews_by_id(review_id):
    """method that deletes a review by id"""
    delete_review = storage.get('Review', review_id)
    if delete_review is None:
        abort(404)
    storage.delete(delete_review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def post_review(place_id):
    """method to post a new place"""
    new_review = request.get_json()
    if not new_review:
        abort(400, 'Not a JSON')
    if 'user_id' not in new_review:
        abort(400, 'Missing user_id')
    if 'text' not in new_review:
        abort(400, 'Missing text')
    my_user = storage.get('User', request.json['user_id'])
    if my_user is None:
        abort(404)
    my_place = storage.get('Place', place_id)
    if my_place is None:
        abort(404)
    new_review = Review(user_id=request.json['user_id'],
                        text=request.json['text'], place_id=place_id)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def put_review(review_id):
    """method to update/put a review by id"""
    mod_review = storage.get('Review', review_id)
    if mod_review is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    req_review = request.get_json()
    for key in req_review:
        if key == 'id' or key == 'user_id' or\
           key == 'place_id' or key == 'created_at' or key == 'updated_at':
            pass
        else:
            setattr(mod_review, key, req_review[key])
    storage.save()
    return jsonify(mod_review.to_dict()), 200
