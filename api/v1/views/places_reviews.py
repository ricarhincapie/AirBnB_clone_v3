#!/usr/bin/python3
"""
Module - Reviews for places view RESTful API
"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_review_by_place(place_id):
    """ get json of the reviews linke to the place given"""
    box = storage.get(Place, place_id)
    if box is None:
        abort(404)
    else:
        my_list = []
        for item in box.reviews:
            my_list.append(item.to_dict())
        return jsonify(my_list), 200


@app_views.route('/reviews/<review_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """ provides review based on given id """
    box = storage.get(Review, review_id)
    if box is None:
        abort(404)
    else:
        return jsonify(box.to_dict()), 200


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ deletes a review based on id given """
    box = storage.get(Review, review_id)
    if box is None:
        abort(404)
    else:
        box.delete()
        storage.save()
        return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """ publish a review of the place spacified """
    review_text = request.get_json()
    place_exist = storage.get(Place, place_id)
    if review_text is None:
        abort(400, 'Not a JSON')
    elif 'text' not in review_text:
        abort(400, 'Missing text')
    elif 'user_id' not in review_text:
        abort(400, 'Missing user_id')
    elif not storage.get(User, review_text.get('user_id')):
        abort(404)
    elif not place_exist:
        abort(404)
    else:
        new_review = Review(**review_text)
        new_review.place_id = place_id
        storage.new(new_review)
        storage.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """ updates a review based on its id given """
    ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    my_dict = request.get_json()
    if not my_dict:
        abort(400, 'Not a JSON')
    box = storage.get(Review, review_id)
    if box is None:
        abort(404)
    else:
        for key in my_dict.keys():
            setattr(box, key, my_dict[key])
        box.save()
        return jsonify(box.to_dict())
