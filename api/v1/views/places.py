api/v1/views/places.py#!/usr/bin/python3
"""
Module - User view RESTful API
"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.place import Place


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_places(city_id=None):
    """Route to handle city/<city_id>/cities GET"""
    my_list = []
    if city_id is None:
        abort(404)
    verify_city = storage.get(City, city_id)
    if verify_city is None:
        abort(404)
    else:
        for value in storage.all('Place').values():
                my_list.append(value.to_dict())
    return jsonify(my_list)


@app_views.route('/places/<place_id>', strict_slashes=False)
def get_place(place_id):
    """Route to handle /place/<place_id> GET"""
    box = storage.get(Place, place_id)
    if box is None:
        abort(404)
    return jsonify(box.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Route to handle /place/<place_id> GET"""
    box = storage.get(Place, place_id)
    if box is None:
        abort(404)
    else:
        storage.delete(box)
        storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """Route to handle /cities/<city_id>/places POST"""
    requ = request.get_json()
    if not requ:
        abort('Not a JSON', 400)
    if not requ.get('user_id'):
        abort('Missing user_id', 400)
    if not requ.get('name'):
        abort('Missing name', 400)
    box = storage.get(City, city_id)
    if box is None:
        abort(404)
    new_place = Place(**requ)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict())


